---
id: b2.kata.stop-orphan-work-and-pool-exhaustion
kind: kata
title: Kata — остановить orphan work и pool exhaustion
owner_track: b2
module: b2.module.performance-resource-control
coverage:
  - target: b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle
    role: practice
  - target: b2.level-outcome.manage-service-resource-lifecycle-l2-design-local-lifecycle
    role: assess
  - target: b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary
    role: practice
  - target: b2.level-outcome.integrate-external-services-l2-design-typical-client-boundary
    role: assess
  - target: b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work
    role: practice
  - target: b2.level-outcome.control-concurrency-cancellation-l2-bound-local-work
    role: assess
  - target: b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck
    role: practice
  - target: b2.level-outcome.diagnose-service-performance-l2-localize-common-bottleneck
    role: assess
  - target: b2.level-outcome.control-service-load-resources-l2-configure-local-bounds
    role: practice
  - target: b2.level-outcome.control-service-load-resources-l2-configure-local-bounds
    role: assess
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: practice
  - target: b2.level-outcome.verify-service-behavior-l2-select-test-boundaries
    role: assess
status: accepted
updated: 2026-08-15
language: ru
last_verified: 2026-08-15
versions:
  python: 3.14.6
  fastapi: 0.136.3
  starlette: 1.3.1
  httpx: 0.28.1
---

# Kata: остановить orphan work и pool exhaustion

Команда `Quote API` получила жалобу: gateway уже вернул клиенту timeout, но сервис продолжает обращаться к `Pricing`, пул остаётся занятым, а следующие запросы ждут всё дольше. Ваша задача — сначала сделать отказ воспроизводимым и измеримым, затем исправить его и доказать отсутствие регрессии.

Kata оценивает типовую самостоятельную работу L2. Она не требует Kubernetes, production telemetry stack или готового эталонного решения.

## Исходная система

Участник самостоятельно создаёт минимальную стартовую систему по этому контракту. Готового репозитория-заготовки (`scaffold repository`) и эталонного решения нет; структура ниже задаёт только независимо проверяемые внешние свойства.

Стартовая система должна содержать:

- FastAPI-приложение с одним endpoint `GET /quotes/{item_id}`;
- отдельную управляемую медленную dependency `Pricing` либо ASGI/mock transport с тем же наблюдаемым HTTP-поведением;
- четыре исходящих вызова на один запрос;
- общий `httpx.AsyncClient` с пулом максимум восемь соединений;
- переключатель задержки: 80 мс обычно и 700 мс для заданной доли вызовов;
- счётчики `active_requests`, `outbound_in_flight`, `outbound_waiting`, `tasks_started`, `tasks_finished`, `tasks_cancelled`;
- нагрузочный test harness, который умеет завершить ожидание клиента на 600 мс и продолжить наблюдение сервиса.

Стартовая реализация намеренно создаёт дочернюю работу без достаточного владения и не имеет согласованного end-to-end deadline. Конкретный дефект scaffold может быть реализован разными способами, но тест обязан показать, что после клиентского timeout часть работы продолжает занимать pool.

## Failure envelope

Не меняйте числа во время первой итерации:

| Параметр | Значение |
|---|---|
| Набор измеряемых запросов и нагрузка | Все входящие запросы `Quote API`: 12 конкурентных запросов, каждый с fan-out 4 |
| Duration | Два контролируемых прогона по 60 секунд; после каждого — 10 секунд наблюдения |
| Здоровый профиль зависимости | Все вызовы `Pricing` занимают около 80 мс |
| Деградированный профиль зависимости | 25% вызовов `Pricing` занимают около 700 мс, остальные — около 80 мс |
| Pool и deadline | Максимум 8 соединений; общий deadline 600 мс; в исправленной конфигурации каждая попытка ждёт соединение не более 100 мс |
| Acceptance здорового профиля | p95 по серверной (`service-side`) метрике `Quote API` для всех запросов 60-секундного прогона, от приёма запроса до исхода обработки на уровне приложения (`application outcome`), ≤ 450 мс |
| Acceptance деградированного профиля | 100% запросов 60-секундного прогона достигают полного ответа, явно неполного/деградированного ответа (`partial/degraded`) либо контролируемой ошибки по той же серверной точке не позднее 650 мс |
| Resource/recovery acceptance | Открытых соединений ≤ 8; waiting/in-flight = 0 не позднее 1 с после снятия нагрузки; отдельный shutdown ≤ 2 с |

Pool wait измеряется от запроса соединения из пула до его получения или `PoolTimeout`. Это acceptance criteria эксперимента, а не production-гарантия для иной нагрузки. Результат с другим workload полезен как дополнительный эксперимент, но не заменяет этот контрольный профиль.

## Ваша задача

### Часть 1. Воспроизвести и измерить

1. Запустите обычный профиль и сохраните p50/p95/p99, причины завершения и максимальные state counters.
2. Включите медленную ветвь и покажите рост pool wait либо очереди.
3. Завершите клиентское ожидание на 600 мс и докажите, продолжается ли downstream work.
4. Снимите нагрузку и измерьте время recovery.
5. Сформулируйте причинную гипотезу до изменения кода.

### Часть 2. Исправить

Спроектируйте решение, которое одновременно:

- задаёт владельца общего HTTP-клиента и его pool;
- связывает дочерние задачи с request scope;
- использует остаток одного deadline, включая очередь и pool wait;
- ограничивает полезную конкурентную работу;
- имеет явное поведение при насыщении;
- освобождает управляемые ресурсы на success, error, cancellation и graceful shutdown.

Не требуется использовать конкретный primitive. Вы можете выбрать `TaskGroup`, semaphore, собственный admission controller или эквивалент, если объясните границы и докажете свойства.

### Часть 3. Доказать

Повторите тот же failure envelope. Предоставьте regression tests и observations, которые показывают:

- дочерние задачи не переживают родительскую операцию без отдельного владельца;
- pool не превышает восемь соединений;
- очередь ограничена временем или размером;
- deadline и overload outcomes различимы;
- после нагрузки waiting/in-flight возвращаются к нулю и управляемые ресурсы освобождаются;
- shutdown укладывается в две секунды.

## Контракт scaffold

Организация файлов свободна, но внешние точки должны позволять независимо проверить решение:

- команда запуска `Quote API` и управляемой dependency;
- команда обычного и деградированного load profile;
- endpoint или test hook для изменения задержки без перезапуска;
- машинно-читаемый снимок counters до/во время/после опыта;
- тест, который инициирует deadline/cancellation;
- тест lifespan/shutdown;
- README с закреплёнными версиями и одной командой полного воспроизведения.

Harness не должен требовать облака. In-process transport допустим для быстрых тестов, но хотя бы одна проверка cancellation/disconnect должна использовать реальную выбранную ASGI server/transport границу, иначе нельзя делать вывод об этой интеграции.

## Что не входит

- готовый код исправления;
- выбор единственного «правильного» числа concurrency;
- retry/circuit breaker как обязательные элементы;
- Kubernetes, autoscaling, service mesh и production IAM;
- база данных и distributed transaction;
- полноценный observability stack;
- доказательство поведения при process kill или удалённом side effect.

## Критерии самопроверки

- [ ] История отказа понятна по README без чтения тестов.
- [ ] Baseline и исправленная версия запускаются одним и тем же harness.
- [ ] Гипотеза сформулирована до tuning.
- [ ] Disconnect, timeout, deadline и cancellation не названы синонимами.
- [ ] Application client создаётся и закрывается в одной lifecycle boundary.
- [ ] Дочерние задачи имеют наблюдаемого владельца.
- [ ] Admission/concurrency/pool limits имеют разные объяснённые обязанности.
- [ ] Любое изменённое число сопровождается workload, duration, dependency behavior и threshold.
- [ ] Тест падает на исходном дефекте и проходит после исправления.
- [ ] Recovery проверяется после, а не только во время нагрузки.
- [ ] Известные пределы cleanup перечислены честно.

## Progressive hints

<details>
<summary>Подсказка 1 — где искать</summary>

Постройте временную шкалу одного входящего запроса и четырёх downstream-вызовов. Отметьте момент клиентского timeout, получение соединения, завершение каждой задачи и release ресурса. Ищите работу, у которой после timeout нет полезного ожидающего владельца.

</details>

<details>
<summary>Подсказка 2 — что измерять</summary>

Одной latency недостаточно. Сопоставьте `outbound_waiting`, `outbound_in_flight`, pool utilization и баланс started/finished/cancelled. Проверьте значения через секунду после снятия нагрузки.

</details>

<details>
<summary>Подсказка 3 — класс подхода</summary>

Рассмотрите структурированную область владения дочерними задачами и один абсолютный deadline. Время ожидания admission и pool должно уменьшать остаток budget, а не добавляться к нему.

</details>

<details>
<summary>Подсказка 4 — перегрузка</summary>

Пул ограничивает соединения, но не обязательно очередь. Определите, где сервис перестаёт принимать новую дорогую работу и какой быстрый исход видит клиент. Не дублируйте один лимит без объяснения.

</details>

<details>
<summary>Подсказка 5 — доказательство</summary>

Сделайте исходный дефект причиной падения теста: после deadline остаётся in-flight работа или shutdown превышает budget. Затем повторите неизменный эксперимент и проверьте state recovery, а не только HTTP-статус.

</details>

## Вопросы после выполнения

### Какая проверка отличила причину от симптома?

<details>
<summary>Что должен раскрыть ответ</summary>

Конкретное изменение одного фактора и совместное наблюдение. Например, при неизменном workload fan-out 1 устранил pool wait, а возвращение fan-out 4 воспроизвело его; propagation cancellation затем убрала остаточные tasks. Фраза «посмотрел графики» недостаточна.

</details>

### Почему ваши concurrency limit и pool size не являются случайным tuning?

<details>
<summary>Что должен раскрыть ответ</summary>

Нужна связь с safe dependency capacity, fan-out, deadline и выбранным overload behavior, затем результат одного и того же load/failure test. Также следует назвать, когда числа потребуется пересмотреть.

</details>

### Чего не доказывает ваша cancellation-проверка?

<details>
<summary>Что должен раскрыть ответ</summary>

Она доказывает только выбранные process/server/framework boundaries. Она не гарантирует остановку blocking/uncancellable кода, process kill и удалённого side effect. In-process test также не доказывает реальный disconnect без отдельной transport-проверки.

</details>

## Словарь

| Термин | Значение в kata |
|---|---|
| Scaffold | Минимальная стартовая система и test harness без готового исправления |
| Failure envelope | Зафиксированные workload, duration, dependency behavior и thresholds |
| Orphan work | Downstream-работа без полезного ожидающего запроса |
| Regression test | Проверка, падающая на исходном дефекте и защищающая исправленное свойство |
| Recovery | Возврат waiting/in-flight к нулю и освобождение управляемых ресурсов после нагрузки |
| Admission | Решение допустить новую работу при текущей загрузке |
| Bounded cleanup | Release управляемых ресурсов в проверяемый срок |

## Первичные источники

- [Python 3.14 — Coroutines and Tasks](https://docs.python.org/3.14/library/asyncio-task.html)
- [FastAPI — Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [Starlette — Requests](https://www.starlette.io/requests/)
- [HTTPX — Resource Limits](https://www.python-httpx.org/advanced/resource-limits/)
- [HTTPX — Timeouts](https://www.python-httpx.org/advanced/timeouts/)
