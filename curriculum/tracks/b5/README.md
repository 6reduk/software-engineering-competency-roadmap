---
id: b5.index.capability-blueprint
kind: index
title: "B5 — capability blueprint первого breadth-pass"
owner_track: b5
status: accepted
updated: 2026-09-20
language: ru
---

# B5 — capability blueprint первого breadth-pass

**B5** — это код пятой технической вертикали группы B: **Distributed Systems**,
то есть распределённые системы. Трек посвящён гарантиям, которые возникают
между несколькими независимо отказывающими участниками: допустимому результату,
праву на действие, доставке и повтору, размещению состояния, устареванию,
перегрузке и совместимости при изменениях. Место B5 среди остальных вертикалей
показано в [общей карте треков](../../program/track-map.md).

## Содержание: 6 модулей B5

Модуль объединяет несколько кластеров вокруг одного проверяемого системного
результата. Ссылка в названии ведёт к scope, capabilities и non-goals. Статус
маршрута отличает готовый учебный срез от одного только blueprint.

| Модуль | Что осваивается | Учебный маршрут |
|---|---|---|
| [Результат при частичном отказе](modules.md#bound-system-guarantees) | Определять участников, неизвестный исход и допустимую видимость состояния | Пока blueprint |
| [Право на действие при смене владельца](modules.md#preserve-authority-across-failures) | Связывать authority, причинный порядок и fencing с допустимостью эффекта | [Готовый срез: stale authority и fencing](slices/stale-authority-fencing/README.md) |
| [Размещение состояния и цена отказа](modules.md#place-state-with-bounded-failure-cost) | Выбирать размещение, репликацию и перенос владения с явными пределами | Пока blueprint |
| [Доставка и бизнес-эффекты](modules.md#compose-delivery-and-business-effects) | Различать доставку, повтор, фиксацию, идемпотентность и компенсацию | Пока blueprint |
| [Устаревание и перегрузка](modules.md#bound-staleness-and-overload) | Ограничивать системную несвежесть cache и распространение лишней работы | Пока blueprint |
| [Сохранение гарантий при эволюции](modules.md#preserve-guarantees-through-change) | Проверять общий договор при смешанных версиях различающими историями | Пока blueprint |

Если нужен готовый материал для самостоятельного прохождения, откройте
[каталог учебных срезов B5](slices/). Полный перечень capabilities и критериев
уровней находится в [capabilities](capabilities.md) и
[LevelOutcomes](level-outcomes.md).

Когда запрос проходит через несколько сервисов и хранилищ, потеря ответа, повтор операции или отставание копии затрудняют ответ на главный вопрос: какой результат система обещает клиенту и при каких отказах это обещание сохраняется? Карта B5 помогает инженеру определить границы такой гарантии, сравнить варианты решения и назвать наблюдения, по которым их можно проверить.

В таблице ниже собраны 11 групп системных задач (кластеров). От знакомой задачи можно перейти к модулю, конкретному инженерному действию (capability), ожидаемым результатам уровней L1–L3 и рабочему сценарию. [Входные условия](prerequisites.md#baseline) поясняют необходимую подготовку, а [ролевые требования](role-requirements.md) — ожидаемые действия Backend и Architecture. Карта описывает ожидаемые способности; фактическое освоение и работоспособность решений требуют отдельных свидетельств.

## Семь файлов

| Файл | Назначение |
|---|---|
| [README.md](README.md) | Навигация по системным задачам и границы карты |
| [modules.md](modules.md) | Шесть модулей по системному результату |
| [capabilities.md](capabilities.md) | Семнадцать канонических действий |
| [level-outcomes.md](level-outcomes.md) | 51 наблюдаемый результат L1–L3 |
| [prerequisites.md](prerequisites.md) | A1/A3, conditional B2/B3, Requires/Related и readiness |
| [scenarios.md](scenarios.md) | Одиннадцать коротких рабочих входов |
| [role-requirements.md](role-requirements.md) | Две проекции, 34 конкретные ссылки на outcomes |

[Coverage map](coverage-map.md) — первый реестр фактических учебных отношений; регистрация M2.3 приведена [ниже](#m2-3-slice).

[Фазовый итог первого прохода B5](phase-closeout.md) — пересчёт, ролевые маршруты и условия возврата к долгу.

<a id="traceability"></a>

## Cluster → module → capabilities → outcomes → scenario

Все IDs ниже полные. В outcome-колонке ссылка ведёт к исчерпывающему разделу с тремя полными IDs L1/L2/L3 конкретной capability; раздел не включает чужие outcomes. Сценарные метки локальны. Шесть модулей объединяют кластеры по единому результату, а не создают курс на каждый термин.

| Cluster | Module | Capabilities | Outcomes | Scenario |
|---|---|---|---|---|
| [Модели отказов](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.failure-models`) | [Определять допустимый результат при частичном отказе](modules.md#bound-system-guarantees) (`b5.module.bound-system-guarantees`) | [Строить модель частичных отказов](capabilities.md#model-partial-failures) (`b5.capability.model-partial-failures`) | [model-partial-failures: L1/L2/L3](level-outcomes.md#model-partial-failures) | [FM01](scenarios.md#fm01) |
| [Согласованность и доступность](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.consistency-availability`) | [Определять допустимый результат при частичном отказе](modules.md#bound-system-guarantees) (`b5.module.bound-system-guarantees`) | [Выбирать договор видимости чтения](capabilities.md#choose-read-guarantees) (`b5.capability.choose-read-guarantees`) | [choose-read-guarantees: L1/L2/L3](level-outcomes.md#choose-read-guarantees) | [CA01](scenarios.md#ca01) |
| [Время, порядок и координация](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.time-order-coordination`) | [Сохранять право на действие при смене владельца](modules.md#preserve-authority-across-failures) (`b5.module.preserve-authority-across-failures`) | [Восстанавливать причинный порядок](capabilities.md#reconstruct-causal-order) (`b5.capability.reconstruct-causal-order`), [Исключать эффекты устаревшего владельца](capabilities.md#exclude-stale-actors) (`b5.capability.exclude-stale-actors`) | [reconstruct-causal-order: L1/L2/L3](level-outcomes.md#reconstruct-causal-order); [exclude-stale-actors: L1/L2/L3](level-outcomes.md#exclude-stale-actors) | [TO01](scenarios.md#to01) |
| [Согласование и лидерство](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.consensus-leadership`) | [Сохранять право на действие при смене владельца](modules.md#preserve-authority-across-failures) (`b5.module.preserve-authority-across-failures`) | [Оценивать границы согласования и смены лидера](capabilities.md#assess-leadership-guarantees) (`b5.capability.assess-leadership-guarantees`) | [assess-leadership-guarantees: L1/L2/L3](level-outcomes.md#assess-leadership-guarantees) | [CL01](scenarios.md#cl01) |
| [Репликация и шардирование](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.replication-sharding`) | [Размещать состояние с явной ценой отказа и роста](modules.md#place-state-with-bounded-failure-cost) (`b5.module.place-state-with-bounded-failure-cost`) | [Выбирать размещение и репликацию состояния](capabilities.md#choose-state-placement) (`b5.capability.choose-state-placement`), [Определять безопасный перенос владения шардами](capabilities.md#plan-shard-ownership-transfer) (`b5.capability.plan-shard-ownership-transfer`) | [choose-state-placement: L1/L2/L3](level-outcomes.md#choose-state-placement); [plan-shard-ownership-transfer: L1/L2/L3](level-outcomes.md#plan-shard-ownership-transfer) | [RS01](scenarios.md#rs01) |
| [Сообщения и события](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.messaging-events`) | [Согласовывать доставку и бизнес-эффекты](modules.md#compose-delivery-and-business-effects) (`b5.module.compose-delivery-and-business-effects`) | [Определять договор доставки и повторного чтения](capabilities.md#define-delivery-contract) (`b5.capability.define-delivery-contract`) | [define-delivery-contract: L1/L2/L3](level-outcomes.md#define-delivery-contract) | [ME01](scenarios.md#me01) |
| [Идемпотентность и повторы](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.idempotency-retries`) | [Согласовывать доставку и бизнес-эффекты](modules.md#compose-delivery-and-business-effects) (`b5.module.compose-delivery-and-business-effects`) | [Ограничивать бизнес-эффекты повторного исполнения](capabilities.md#bound-repeat-effects) (`b5.capability.bound-repeat-effects`), [Ограничивать распространение повторов и устойчиво неуспешной работы](capabilities.md#control-retry-propagation) (`b5.capability.control-retry-propagation`) | [bound-repeat-effects: L1/L2/L3](level-outcomes.md#bound-repeat-effects); [control-retry-propagation: L1/L2/L3](level-outcomes.md#control-retry-propagation) | [IR01](scenarios.md#ir01) |
| [Кеширование и управление нагрузкой](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.caching-load-control`) | [Ограничивать распространение устаревания и перегрузки](modules.md#bound-staleness-and-overload) (`b5.module.bound-staleness-and-overload`) | [Определять системную границу устаревания кеша](capabilities.md#bound-cache-staleness) (`b5.capability.bound-cache-staleness`), [Управлять нагрузкой и деградацией между участниками](capabilities.md#control-system-load) (`b5.capability.control-system-load`) | [bound-cache-staleness: L1/L2/L3](level-outcomes.md#bound-cache-staleness); [control-system-load: L1/L2/L3](level-outcomes.md#control-system-load) | [LC01](scenarios.md#lc01) |
| [Распределённые транзакции](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.distributed-transactions`) | [Согласовывать доставку и бизнес-эффекты](modules.md#compose-delivery-and-business-effects) (`b5.module.compose-delivery-and-business-effects`) | [Согласовывать фиксацию состояния и публикацию](capabilities.md#compose-state-and-publication) (`b5.capability.compose-state-and-publication`), [Выбирать границу атомарности и компенсации](capabilities.md#choose-cross-system-atomicity) (`b5.capability.choose-cross-system-atomicity`) | [compose-state-and-publication: L1/L2/L3](level-outcomes.md#compose-state-and-publication); [choose-cross-system-atomicity: L1/L2/L3](level-outcomes.md#choose-cross-system-atomicity) | [DT01](scenarios.md#dt01) |
| [Мощность и несколько регионов](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.capacity-multi-region`) | [Размещать состояние с явной ценой отказа и роста](modules.md#place-state-with-bounded-failure-cost) (`b5.module.place-state-with-bounded-failure-cost`) | [Оценивать системную ёмкость и региональный компромисс](capabilities.md#assess-regional-capacity) (`b5.capability.assess-regional-capacity`) | [assess-regional-capacity: L1/L2/L3](level-outcomes.md#assess-regional-capacity) | [CM01](scenarios.md#cm01) |
| [Эволюция и проверка гарантий](../catalog/b5-distributed-systems.md#clusters) (`b5.cluster.evolution-verification`) | [Сохранять межсистемный договор при эволюции](modules.md#preserve-guarantees-through-change) (`b5.module.preserve-guarantees-through-change`) | [Сохранять договор при смешанных версиях](capabilities.md#preserve-mixed-version-contract) (`b5.capability.preserve-mixed-version-contract`), [Проектировать различающие проверки системной гарантии](capabilities.md#design-distinguishing-histories) (`b5.capability.design-distinguishing-histories`) | [preserve-mixed-version-contract: L1/L2/L3](level-outcomes.md#preserve-mixed-version-contract); [design-distinguishing-histories: L1/L2/L3](level-outcomes.md#design-distinguishing-histories) | [EV01](scenarios.md#ev01) |

Итого: **6 modules / 17 capabilities / 51 outcomes / 11 scenarios / 34 role links**. L1/L2/L3 — по 17; L4/L5 — 0. Role links: 24 required / 5 deepening / 5 conditional. [Обоснование уровней](level-outcomes.md) отделяет модель от реального adoption. [Hard DAG](prerequisites.md#hard-dag): 17 узлов, 5 Requires, без циклов; 8 Related не входят в DAG.

<a id="notation"></a>

## Aggregate catalog notation

Компактная форма следует [примеру B3](../b3/README.md#aggregate-catalog-notation), [entities](../../../governance/architecture/metamodel/entities.md), [relationships](../../../governance/architecture/metamodel/relationships-and-invariants.md), [identifiers](../../../governance/architecture/metamodel/identifiers.md) и [metadata](../../../governance/architecture/metamodel/metadata.md), без копирования предметного состава B3.

- README — `b5.index.capability-blueprint`, `kind: index`. Остальные шесть файлов — агрегированные governance-каталоги с уникальным `artifact`; они не создают учебные artifacts.
- Для всех records наследуются owner_track, status, updated и language из front matter; эти defaults не переопределяются неявно. `kind` берётся из kind-сегмента semantic ID.
- Module: heading задаёт id/title; тело — scope, clusters, develops и non-goals. Runtime baseline не проверен, поэтому `verified_baseline` и `versions` отсутствуют.
- Capability: строка задаёт id/title, primary_cluster, действие и единственный primary module. Related вынесены отдельно без копий capability.
- Outcome: heading раздела задаёт родительскую capability; строка — id, level, title/действие, контекст и evidence criteria. Самостоятельность уровня определена во вводной каталога и применяется к каждой строке.
- Scenario — локальная метка и anchor, не semantic entity нового kind. Role link — одна строка с одним полным outcome ID, категорией и предметным основанием; RoleView адресуется существующим route path без нового ID.
- Requires направлен от зависимой capability к prerequisite; Related — `relates-to`. URL внешних repositories и placeholder capability IDs не выдумываются.

## Ownership и предел глубины G29

| Владелец | Сохраняемая граница |
|---|---|
| [B2](../catalog/b2-backend-api.md) | Service/API contract и прикладная интеграция retry, messaging, cache и abuse controls |
| [B3](../catalog/b3-transactional-data.md) | Локальная транзакция, store isolation, tuning, engine internals, replication/recovery mechanics конкретного store |
| B5 | Межсистемная гарантия, участники, допустимые истории, координация, placement и независимость отказов; компромисс между участниками |
| [B6](../catalog/b6-platform-cloud.md) | Cloud/Kubernetes implementation, provisioning и deployment automation |
| [B7](../catalog/b7-reliability-production.md) | SLO, incident process, production recovery, RTO/RPO strategy и эксплуатационный допуск |
| [C1](../catalog/c1-leadership-architecture.md) | Организационная стратегия, межкомандное исполнение и портфель решений |

Шов replication B3/B5 не определяется числом узлов: B3 сохраняет механику конкретного store, B5 — системную гарантию, placement, независимость отказов и допустимые истории. Наличие B3-материала не является B5 coverage или proficiency.

Consensus/leadership, distributed transactions и multi-region здесь ограничены моделями, применимостью, наблюдаемыми историями и trade-offs. Нет формальных доказательств протоколов, реализации consensus, production topology, cloud provisioning или operational runbook. Системная capacity-модель не является эксплуатационным нормативом. Численные thresholds и технический допуск не назначены.

## Таксономия типов решений и screening

Это конечный словарь сравнения, без новых semantic IDs:

| Тип решения | Различаемый предмет | Примеры в карте |
|---|---|---|
| Композиция доставки и бизнес-эффекта | Где доставка перестаёт доказывать результат операции | ME01, IR01, DT01 |
| Координация владения/лидерства | Кто вправе менять ресурс и где исключается старый участник | TO01, CL01 |
| Договор видимости/согласованности чтения | Какое состояние вправе наблюдать клиент и какой ценой | CA01 |
| Размещение, репликация, независимость отказов | Где состояние остаётся доступно при изменении участников | RS01, CM01 |
| Управление нагрузкой и деградацией | Как ограничить усиление работы и распространение отказа | LC01, IR01 |

Failure models и evolution/verification дают поперечные действия анализа и проверки этих пяти типов, без второй классификации semantic entities.

Рекомендуются **три неранжированных кандидата** на последующее сравнение. Ни первый, ни второй slice не выбран; таблица не является заказом реализации.

| Кандидат | Тип, гарантия и различающее наблюдение | Результат для Backend / Architecture | Риск дубля и readiness |
|---|---|---|---|
| Заказ, публикация и эффект после потери acknowledgement (ME01/IR01/DT01) | Композиция: связать commit, доставку и фактический эффект; различить повтор сообщения и повтор бизнес-действия | Backend — договор повторного эффекта; Architecture — предел композиции и ответственность участников | Повтор SDK/SQL outbox остаётся B2/B3; нужны связанные следы независимых границ, доступность не проверена |
| Старый исполнитель после передачи владения (TO01/CL01) | Координация: различить знание лидера и право эффекта; наблюдать принятую/отклонённую запись старого исполнителя | Backend — защита границы эффекта; Architecture — выбор authority и цены прекращения progress | Локальный mutex не даёт новое B5 reasoning; нужны управляемая пауза и наблюдаемый ресурс, доступность не проверена |
| Чтение через другой узел после записи (CA01) | Видимость: связать подтверждение и клиентские чтения при отставании; отличить нарушение договора от допустимого старого значения | Backend — договор клиентского пути; Architecture — компромисс свежести, задержки и доступности | Store-specific tuning остаётся B3; нужны причинные следы и независимые точки чтения, доступность не проверена |

В отдельном будущем решении второй slice допустим только при смене типа решения, гарантии, различающих наблюдений и новом результате для обеих ролей, который не доказан первым. Замена брокера/БД при прежнем результате контраста не даёт. После принятия карты сохраняется предел: один slice → явное решение о втором → обязательный close-out; после второго третьего нет. Эти шаги требуют отдельного назначения.

<a id="decision-record"></a>

## Decision record: границы этого blueprint и C1-линза

Статус записи — **авторское обоснование**, не принятие и не результат межкомандного исполнения. Контекст: нужен один компактный batch всех 11 кластеров при семи файлах. Рассмотрены один module на кластер и группировка по результату. Выбрана группировка в шесть modules с единственным primary owner каждого действия и явной трассировкой. Гарантия документа — различимость и адресуемость ожидаемых результатов; runtime-гарантия этой записью не установлена. Предположение об отказах для предмета карты — участники могут независимо останавливаться, терять связь и подтверждения; корреляция отказов требует отдельного анализа, независимость не принимается по числу копий. Цена группировки — более плотная навигация. Сигнал пересмотра — reviewer не может восстановить цепочку cluster → действие → outcome либо обнаруживает два несовместимых результата одного модуля.

| Поле C1-линзы | Авторское содержание и граница факта |
|---|---|
| Заинтересованные стороны | Backend нужна проверяемая граница подсистемы; Architecture — цена и ответственность системного договора. Это проектные роли, не подтверждённые участники реального внедрения |
| Рассмотренные альтернативы | Одиннадцать модулей дают прямую навигацию, шесть уменьшают дробление связанных результатов; второй вариант выбран для карты, не для deep slice |
| Ownership | Автор отвечает за семь файлов; оркестратор — за acceptance и следующий мандат; независимые reviewers — за собственные выводы. Владельцы реального adoption не подтверждены; оркестратор уточняет их только при назначении соответствующей работы |
| Стоимость риска | Слишком широкое объединение скрывает границы; атомизация раздувает сопровождение. Численная стоимость не подтверждена; оркестратор уточняет её по замечаниям traceability review и трудозатратам навигации |
| Обратимость | Названия и группировку можно исправить до acceptance с сохранением смысла IDs; семантические замены после принятия требуют metamodel alias/supersession. Сигнал пересмотра назван выше |
| Передача знания | Получатели — оркестратор и два будущих reviewer-профиля; передаются семь файлов, таблица трассировки и различия ролей. Получатель проверяет путь от любого кластера к outcome без помощи автора; фактическая передача/понимание не подтверждены, оркестратор получает это свидетельство в review |

Будущий B5 decision record центрального решения хранится **в составе проектного артефакта отдельно назначенного slice**, в разделе «Decision record» с подразделом «C1-линза». Он сохраняет контекст, варианты, выбранную гарантию, предположения об отказах, цену и сигнал пересмотра, а также эти шесть полей intake. Файл или путь будущего артефакта сейчас не создаётся и не назначается.

На close-out проверяются разрешающиеся ссылки на эту запись blueprint и записи фактически созданных slices, шесть непустых полей и статус факта: авторское обоснование, учебное требование или выполненная работа. Для неизвестного — «не подтверждено», владелец уточнения и способ проверки; для остановленного slice — причина отсутствия решения и владелец долга. Комплектность не доказывает качество альтернатив, передачу знания, C1 capability, coverage, proficiency или L4/L5 evidence.

<a id="handoff"></a>

## Статус карты и граница аудита

Карта создана одним общим breadth-pass по [M2.2](../../../governance/work-packages/M2.2-b5-capability-breadth-pass.md) в границах G29 и [принята после G30](../../../governance/reviews/M2.2-G30-b5-capability-breadth-pass-acceptance.md). Acceptance относится к качеству blueprint: coverage, proficiency, завершение модулей, Gate 0 и runtime evidence не заявлены. SHA-256 подтверждает неизменность только в измеренном интервале; история до исходного снимка — `NOT_VERIFIED`.

<a id="m2-3-slice"></a>

## Регистрация M2.3: устаревший владелец и fencing

По [назначению после G30](../../../governance/reviews/M2.2-G30-b5-capability-breadth-pass-acceptance.md) создан первый [пятижанровый маршрут](slices/stale-authority-fencing/README.md) TO01 с ограниченным CL01. Первая серия и первоначальная запись [Gate 0 M2.3](../../../governance/work-packages/M2.3-stale-authority-fencing-slice.md#gate-0-record) были выполнены до создания материалов. При авторской самопроверке выяснилось, что сообщение `prepared` не доказывало сохранение конкретного payload. Оснастка была исправлена, после чего полная серия 10 control / 10 defect / 10 fixed повторена уже после создания материалов. Таблица цепочек, 45.257 секунды, PID и hashes относятся к финальной серии. Повтор не устраняет нарушение обязательного порядка Gate 0 → authoring. После двухпрофильного G31 и точечной проверки M2.3a [пять материалов и coverage map приняты](../../../governance/reviews/M2.3-G31-stale-authority-fencing-acceptance.md): 35 отношений к 11 targets.

Регистрация относится к M2.3. Утверждения выше о невыбранных кандидатах и непроверенной среде описывают состояние breadth-pass M2.2 и не отменяют отдельного назначения/опыта M2.3. Blueprint-каталоги и их статусы не изменены. Acceptance подтверждает материалы и coverage, но не proficiency, выполнение заданий, module completion, ImplementationReference или production readiness. Второй slice не выбран.
