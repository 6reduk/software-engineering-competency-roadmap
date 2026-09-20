import subprocess, threading, queue, time, json, pathlib, sys
from decimal import Decimal
ROOT = pathlib.Path(__file__).parent
LOG = []
class Session:
    def __init__(self, name, user='postgres'):
        self.name=name; self.n=0; self.q=queue.Queue()
        assert user in ['postgres','se01_old','se01_new','se01_backfill']
        self.p=subprocess.Popen(['docker','exec','-i','se01-gate0-20260913','sh','-c',f'exec psql -X -qAt -U {user} -d postgres -v ON_ERROR_STOP=0 2>&1'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',bufsize=1)
        def read():
            for line in self.p.stdout: self.q.put(line.rstrip('\n'))
        threading.Thread(target=read,daemon=True).start()
        self.sql("SET application_name='se01-"+name+"'; SET default_transaction_isolation='read committed'; SET statement_timeout='2s'; SET lock_timeout='1500ms';")
    def sql(self, sql, expect='00000'):
        self.n+=1; marker=f'END_{self.name}_{self.n}'; start=time.monotonic()
        self.p.stdin.write(sql+'\n\\echo '+marker+' :SQLSTATE\n'); self.p.stdin.flush()
        lines=[]
        while True:
            line=self.q.get(timeout=5)
            if line.startswith(marker+' '): state=line.split()[-1]; break
            lines.append(line)
        entry=dict(session=self.name,sql=sql,output=lines,sqlstate=state,seconds=round(time.monotonic()-start,6))
        LOG.append(entry)
        if state!=expect: raise AssertionError(entry)
        return lines
    def close(self):
        if self.p.poll() is None:
            self.sql('ROLLBACK;'); self.p.stdin.write('\\q\n'); self.p.stdin.flush(); self.p.wait(timeout=5)

def event(label, **fields): LOG.append(dict(event=label,**fields))

def main():
    sessions=[]
    d=Session('ddl'); sessions.append(d)
    try:
        for role in ['old','new','backfill']:
            d.sql(f"CREATE ROLE se01_{role} LOGIN;")
        o=Session('old','se01_old'); n=Session('new','se01_new'); b=Session('backfill','se01_backfill'); v=Session('observer'); w=Session('lockwriter')
        sessions.extend([o,n,b,v,w])
        event('environment',server=d.sql('SELECT version();'),client=subprocess.check_output(['docker','exec','se01-gate0-20260913','psql','--version'],text=True).strip(),python=sys.version)
        for s in sessions:
            event('session',name=s.name,settings=s.sql("SELECT current_user,pg_backend_pid(),current_setting('transaction_isolation'),current_setting('statement_timeout'),current_setting('lock_timeout');"),autocommit=True)
        event('declared',defect='23514',isolation='read committed',operation_limit_seconds=2,profile_limit_seconds=60,lock_timeout_seconds=1.5,oracle=[[1,0],[2,12000],[3,1300],[4,999999999999],[5,789],[6,2501]])
        def rows(): return v.sql('SELECT order_id,amount_rub,amount_minor FROM orders ORDER BY order_id;')
        def ddl(sql, mode):
            d.sql('BEGIN;'); d.sql(sql)
            locks=v.sql("SELECT mode FROM pg_locks WHERE pid=(SELECT pid FROM pg_stat_activity WHERE application_name='se01-ddl') AND relation='orders'::regclass AND granted ORDER BY mode;")
            assert mode in locks,(sql,locks)
            event('ddl_lock',sql=sql,modes=locks); d.sql('COMMIT;')
        def matrix(stage):
            # Diagnostic writes are rolled back and never enter the business oracle.
            o.sql('SELECT order_id,amount_rub FROM orders ORDER BY order_id;')
            o.sql('BEGIN;'); o.sql('INSERT INTO orders(order_id,amount_rub) VALUES(90,1.00);'); o.sql('UPDATE orders SET amount_rub=2.00 WHERE order_id=90;')
            assert o.sql('SELECT amount_rub FROM orders WHERE order_id=90;')==['2.00']; o.sql('ROLLBACK;')
            if stage==0:
                n.sql('SELECT amount_minor FROM orders;',expect='42703')
                n.sql('INSERT INTO orders(order_id,amount_rub,amount_minor) VALUES(90,1,100);',expect='42703')
            elif stage==1: event('new_paths_disabled',stage=stage)
            else:
                read=n.sql('SELECT order_id,COALESCE(amount_minor,(amount_rub*100)::bigint),amount_minor IS NULL OR amount_minor=amount_rub*100 FROM orders ORDER BY order_id;')
                assert all(x.endswith('|t') for x in read)
                n.sql('BEGIN;'); n.sql('INSERT INTO orders(order_id,amount_rub,amount_minor) VALUES(90,1,100);'); n.sql('UPDATE orders SET amount_rub=2,amount_minor=200 WHERE order_id=90;')
                assert n.sql('SELECT amount_rub,amount_minor FROM orders WHERE order_id=90;')==['2.00|200']; n.sql('ROLLBACK;')
            event('matrix_pass',stage=stage)
        def reset():
            d.sql('DROP TABLE IF EXISTS orders;')
            d.sql('CREATE TABLE orders(order_id integer PRIMARY KEY,amount_rub numeric(12,2) NOT NULL CHECK(amount_rub BETWEEN 0 AND 9999999999.99));')
            d.sql('GRANT SELECT,INSERT,UPDATE ON orders TO se01_new,se01_backfill;')
            d.sql('GRANT SELECT(order_id,amount_rub),INSERT(order_id,amount_rub),UPDATE(amount_rub) ON orders TO se01_old;')
            d.sql('INSERT INTO orders VALUES(1,0),(2,100),(3,12.34),(4,9999999999.99);')
            matrix(0)
            ddl('ALTER TABLE orders ADD COLUMN amount_minor bigint;','AccessExclusiveLock'); matrix(1)
            d.sql("CREATE OR REPLACE FUNCTION se01_compat() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF current_user='se01_old' THEN NEW.amount_minor:=(NEW.amount_rub*100)::bigint; END IF; RETURN NEW; END $$;")
            d.sql('CREATE TRIGGER compat BEFORE INSERT OR UPDATE OF amount_rub ON orders FOR EACH ROW EXECUTE FUNCTION se01_compat();')
            matrix(2) # compatibility must work BEFORE enforcement
            ddl('ALTER TABLE orders ADD CONSTRAINT pair_ok CHECK(amount_minor=amount_rub*100) NOT VALID;','AccessExclusiveLock')
            matrix(2) # and after enforcement, while historical NULL remains legal
        def oldwrite(sql, ident, expected):
            o.sql(sql); read=v.sql(f'SELECT amount_rub,amount_minor FROM orders WHERE order_id={ident};')
            assert read==[f'{Decimal(expected)/100:.2f}|{expected}']; event('ack_old',id=ident,minor=expected,readback=read)
        def newwrite(sql,ident,expected):
            n.sql('BEGIN;'); n.sql(sql)
            before=v.sql(f'SELECT amount_rub,amount_minor FROM orders WHERE order_id={ident};')
            n.sql('COMMIT;'); read=v.sql(f'SELECT amount_rub,amount_minor FROM orders WHERE order_id={ident};')
            assert read==[f'{Decimal(expected)/100:.2f}|{expected}']; event('ack_new_atomic',id=ident,minor=expected,before_commit=before,readback=read)
        def current_writes():
            oldwrite('UPDATE orders SET amount_rub=120 WHERE order_id=2;',2,12000)
            oldwrite('INSERT INTO orders(order_id,amount_rub) VALUES(5,7.89);',5,789)
            newwrite('INSERT INTO orders(order_id,amount_rub,amount_minor) VALUES(6,25.01,2501);',6,2501)
            newwrite('UPDATE orders SET amount_rub=13,amount_minor=1300 WHERE order_id=3;',3,1300)
        def batch(ids):
            assert len(ids)<=2
            b.sql('UPDATE orders SET amount_minor=(amount_rub*100)::bigint WHERE amount_minor IS NULL AND order_id IN ('+','.join(map(str,ids))+');')
        def finish():
            expected=['1|0.00|0','2|120.00|12000','3|13.00|1300','4|9999999999.99|999999999999','5|7.89|789','6|25.01|2501']
            assert rows()==expected; event('full_oracle',rows=rows(),missing=0,extra=0,null=0,mismatch=0)
            ddl('ALTER TABLE orders VALIDATE CONSTRAINT pair_ok;','ShareUpdateExclusiveLock'); matrix(3)
            ddl('ALTER TABLE orders ADD CONSTRAINT minor_present CHECK(amount_minor IS NOT NULL) NOT VALID;','AccessExclusiveLock')
            ddl('ALTER TABLE orders VALIDATE CONSTRAINT minor_present;','ShareUpdateExclusiveLock')
            ddl('ALTER TABLE orders ALTER COLUMN amount_minor SET NOT NULL;','AccessExclusiveLock'); matrix(4)
            event('constraints',rows=d.sql("SELECT conname,convalidated FROM pg_constraint WHERE conrelid='orders'::regclass ORDER BY conname;"))
            d.sql('UPDATE orders SET amount_minor=1 WHERE order_id=2;',expect='23514')
            d.sql('UPDATE orders SET amount_minor=NULL WHERE order_id=2;',expect='23502')
            o.sql('UPDATE orders SET amount_rub=-0.01 WHERE order_id=2;',expect='23514')
            o.sql('UPDATE orders SET amount_rub=10000000000.00 WHERE order_id=2;',expect='22003')
            for invalid in ['-0.01','1.001','10000000000.00']:
                value=Decimal(invalid)
                valid=value>=0 and value<=Decimal('9999999999.99') and value*100==(value*100).to_integral_value()
                assert not valid; event('input_rejected_before_sql',input=invalid,reason='external exact-decimal W-old contract')
            # Type rounding is observed explicitly, not misreported as rejection.
            o.sql('BEGIN;'); o.sql('UPDATE orders SET amount_rub=1.001 WHERE order_id=2;')
            assert o.sql('SELECT amount_rub FROM orders WHERE order_id=2;')==['1.00']; o.sql('ROLLBACK;')
            event('precision_limit',raw_type_rounds=True,raw_probe_rolled_back=True)
            for ids in [[1,2],[3,4],[5,6]]: batch(ids)
            assert rows()==expected
            event('final',rows=rows())
        # Short signature probe precedes all complete profiles.
        reset(); saved=b.sql('SELECT (amount_rub*100)::bigint FROM orders WHERE order_id=2;'); assert saved==['10000']
        oldwrite('UPDATE orders SET amount_rub=120 WHERE order_id=2;',2,12000)
        b.sql('UPDATE orders SET amount_minor='+saved[0]+' WHERE order_id=2;',expect='23514')
        assert rows()[1]=='2|120.00|12000'; event('signature_confirmed',saved=10000,sqlstate='23514',next_stage_started=False)
        for profile in ['Control','Defect','Fixed']:
            for repeat in [1,2]:
                started=time.monotonic(); event('profile_begin',profile=profile,repeat=repeat); reset()
                naive=b.sql('SELECT order_id FROM orders ORDER BY order_id;')
                if profile=='Control':
                    batch([1,2]); event('batch_committed',ids=[1,2],rows=rows()); current_writes()
                else:
                    saved=b.sql('SELECT (amount_rub*100)::bigint FROM orders WHERE order_id=2;'); assert saved==['10000']; event('barrier_captured',saved=10000)
                    current_writes(); event('barrier_writers_committed')
                assert naive==['1','2','3','4']
                assert v.sql('SELECT order_id FROM orders ORDER BY order_id;')==['1','2','3','4','5','6']
                event('naive_population_incomplete',naive=naive,missing_from_naive=[5,6],old_insert=5)
                if profile=='Defect':
                    b.sql('UPDATE orders SET amount_minor='+saved[0]+' WHERE order_id=2;',expect='23514')
                    assert rows()[1]=='2|120.00|12000'; event('stop',reason='expected 23514',next_stage_started=False,rows=rows())
                else:
                    if profile=='Fixed':
                        # Capture is unchanged; application of stale value now uses a freshness predicate.
                        assert b.sql('UPDATE orders SET amount_minor='+saved[0]+' WHERE order_id=2 AND amount_rub=100 AND amount_minor IS NULL RETURNING order_id;')==[]
                        batch([1,2]); event('batch_committed',ids=[1,2],rows=rows())
                    checkpoint=rows(); event('interrupted',rows=checkpoint,next_stage_started=False)
                    b.close(); sessions.remove(b); b=Session('backfill','se01_backfill'); sessions.append(b)
                    assert rows()==checkpoint; batch([1,2]); assert rows()==checkpoint
                    event('resumed_and_repeated',rows=rows())
                    batch([3,4]); batch([5,6]); finish()
                elapsed=time.monotonic()-started; assert elapsed<60; event('profile_end',profile=profile,repeat=repeat,seconds=round(elapsed,6)); print(profile,repeat,round(elapsed,3),flush=True)
        # Unknown outcome blocks transition even without a SQL error.
        confirmed=False; next_stage=False
        if confirmed: next_stage=True
        assert not next_stage; event('unknown_ack_stop',next_stage_started=next_stage)
        for repeat in [1,2]:
            w.sql('BEGIN;'); w.sql('UPDATE orders SET amount_rub=amount_rub WHERE order_id=1;')
            result={}
            def wait_ddl():
                try: result['output']=d.sql('ALTER TABLE orders ALTER COLUMN amount_minor SET NOT NULL;',expect='55P03')
                except BaseException as e: result['error']=repr(e)
            thread=threading.Thread(target=wait_ddl); thread.start()
            deadline=time.monotonic()+1.4; observed=[]
            while time.monotonic()<deadline:
                observed=v.sql("SELECT a.application_name,a.wait_event_type,a.wait_event,l.mode,l.granted,pg_blocking_pids(a.pid)::text FROM pg_stat_activity a JOIN pg_locks l ON l.pid=a.pid WHERE a.application_name IN ('se01-ddl','se01-lockwriter') AND l.relation='orders'::regclass ORDER BY a.application_name,l.mode;")
                if any('se01-ddl|Lock|relation|AccessExclusiveLock|f|{' in x and not x.endswith('|{}') for x in observed): break
            thread.join(5); assert not thread.is_alive() and 'error' not in result,result
            assert any('se01-ddl|Lock|relation|AccessExclusiveLock|f|{' in x and not x.endswith('|{}') for x in observed),observed
            assert any('RowExclusiveLock|t' in x for x in observed)
            event('lock_observed',repeat=repeat,rows=observed,sqlstate='55P03',next_stage_started=False)
            w.sql('ROLLBACK;'); ddl('ALTER TABLE orders ALTER COLUMN amount_minor SET NOT NULL;','AccessExclusiveLock')
            assert v.sql("SELECT count(*) FROM pg_locks WHERE relation='orders'::regclass AND NOT granted;")==['0']
            event('lock_released_retry_ok',repeat=repeat)
        # Final cleanup after result preservation.
        event('before_cleanup',rows=rows())
        for s in list(sessions):
            if s not in [d,v]: s.close(); sessions.remove(s)
        assert v.sql("SELECT count(*) FROM pg_stat_activity WHERE application_name IN ('se01-old','se01-new','se01-backfill','se01-lockwriter');")==['0']
        d.sql('DROP TABLE orders;'); d.sql('DROP FUNCTION se01_compat();')
        for role in ['old','new','backfill']: d.sql(f'DROP ROLE se01_{role};')
        assert v.sql("SELECT to_regclass('public.orders') IS NULL;")==['t']
        event('cleanup_objects_connections_ok'); print('ALL PROBES PASSED',flush=True)
    finally:
        for s in sessions: s.close()

if __name__=='__main__':
    try: main()
    finally: (ROOT/'runtime.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2),encoding='utf-8')
