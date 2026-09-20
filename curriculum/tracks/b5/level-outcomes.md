---
artifact: b5-level-outcomes-blueprint
title: "Наблюдаемые результаты B5"
owner_track: b5
status: accepted
updated: 2026-09-17
language: ru
---

# Наблюдаемые результаты B5

Критерии описывают ожидаемый рабочий результат независимо от учебного артефакта; они не являются уже полученным evidence. [Metadata и наследование](README.md#notation) едины для всех записей. В каждом разделе capability задаёт родителя, title outcome равен тексту действия.

L1: объяснение заданной истории с поддержкой. L2: самостоятельное ограниченное решение при явных условиях. L3: самостоятельный выбор и защита в границе подсистемы при неопределённости и конкурирующих ограничениях. Эти условия самостоятельности входят в каждую строку соответствующего уровня.

<a id="model-partial-failures"></a>

## `b5.capability.model-partial-failures` — Строить модель частичных отказов

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.model-partial-failures-l1-explain-history` | L1 | По заданной истории объясняет неизвестный исход операции после timeout | Различены истории с эффектом и без эффекта при одинаковом клиентском симптоме; timeout не назван доказанным rollback. |
| `b5.level-outcome.model-partial-failures-l2-define-bounded-model` | L2 | Строит модель отказов ограниченной цепочки вызовов | Названы независимые участники, подтверждения, сохранённые состояния, safety и условия progress; указано недостающее наблюдение для каждого неопределённого исхода. |
| `b5.level-outcome.model-partial-failures-l3-defend-tradeoff` | L3 | Защищает модель при неполных следах и возможном общем источнике отказа | Сравнены конкурирующие объяснения, независимый и коррелированный отказ; названы предел вывода и цена получения различающих наблюдений. |

<a id="choose-read-guarantees"></a>

## `b5.capability.choose-read-guarantees` — Выбирать договор видимости чтения

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.choose-read-guarantees-l1-explain-history` | L1 | Объясняет заданное чтение после подтверждённой записи | Отличены read-your-writes, монотонное чтение, eventual convergence и линеаризуемость; обещание сессии не выдано за глобальное. |
| `b5.level-outcome.choose-read-guarantees-l2-define-bounded-model` | L2 | Задаёт договор чтения для одного клиентского пути | Указаны участники, граница сессии, разрешённые и запрещённые истории, поведение при разрыве связи и после восстановления. |
| `b5.level-outcome.choose-read-guarantees-l3-defend-tradeoff` | L3 | Выбирает гарантию при конфликте свежести, доступности и задержки | Альтернативы сравнены отдельно при partition и без него в логике CAP/PACELC; защищена цена ожидания либо отказа; универсального обещания при любых отказах нет. |

<a id="reconstruct-causal-order"></a>

## `b5.capability.reconstruct-causal-order` — Восстанавливать причинный порядок

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.reconstruct-causal-order-l1-explain-history` | L1 | Объясняет порядок событий в заданном следе | Локальный порядок и send/receive отделены от wall-clock timestamps; неупорядоченная пара не названа причинно связанной. |
| `b5.level-outcome.reconstruct-causal-order-l2-define-bounded-model` | L2 | Строит частичный порядок ограниченной истории | Указаны события, сообщения, причинные рёбра и конкурентные пары; выбран достаточный способ различать события без выдуманного глобального времени. |
| `b5.level-outcome.reconstruct-causal-order-l3-defend-tradeoff` | L3 | Выбирает модель порядка при неполных наблюдениях | Сопоставлены причинный и полный порядок с ценой координации; показано, какой дополнительный порядок нужен инварианту и что останется неизвестным. |

<a id="exclude-stale-actors"></a>

## `b5.capability.exclude-stale-actors` — Исключать эффекты устаревшего владельца

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.exclude-stale-actors-l1-explain-history` | L1 | Объясняет историю возобновления старого исполнителя | Различены истечение lease, мнение исполнителя о владении и принятие записи ресурсом; пауза не считается остановкой старого процесса. |
| `b5.level-outcome.exclude-stale-actors-l2-define-bounded-model` | L2 | Определяет границу проверки полномочий для одного общего ресурса | Названы выдача полномочия, перенос владения, проверяющий участник и запрещённое старое действие; предположения о времени явно записаны. |
| `b5.level-outcome.exclude-stale-actors-l3-defend-tradeoff` | L3 | Защищает исключение устаревшего участника при разделении связи | Сравнены варианты authority и отказа от прогресса; учтён обход проверки и неизвестный исход старой записи; безопасность не выведена только из выбора лидера. |

<a id="assess-leadership-guarantees"></a>

## `b5.capability.assess-leadership-guarantees` — Оценивать границы согласования и смены лидера

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.assess-leadership-guarantees-l1-explain-history` | L1 | Объясняет заданную смену лидера | Различены election, подтверждение решения и внешний эффект; названы предположения об участниках и доступной связи. |
| `b5.level-outcome.assess-leadership-guarantees-l2-define-bounded-model` | L2 | Оценивает применимость заданной модели согласования к ограниченной задаче | Зафиксированы crash/partition assumptions, quorum и разрешённые истории подтверждений; остановка прогресса отделена от нарушения safety. |
| `b5.level-outcome.assess-leadership-guarantees-l3-defend-tradeoff` | L3 | Защищает выбор согласования при конфликте доступности и единого решения | Сравнены координация и ослабление требования; учтены потеря большинства и цена смены лидера; вывод ограничен моделью, без формального доказательства и реализации consensus. |

<a id="choose-state-placement"></a>

## `b5.capability.choose-state-placement` — Выбирать размещение и репликацию состояния

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.choose-state-placement-l1-explain-history` | L1 | Объясняет заданную потерю узла с репликами | Число копий отделено от числа независимых failure domains; подтверждение записи отделено от видимости каждой копии. |
| `b5.level-outcome.choose-state-placement-l2-define-bounded-model` | L2 | Строит модель placement ограниченного набора данных | Указаны владельцы, копии, путь подтверждения и чтения; показаны допустимые исходы потери домена и цена дополнительной копии. |
| `b5.level-outcome.choose-state-placement-l3-defend-tradeoff` | L3 | Защищает размещение при коррелированных отказах и перекосе нагрузки | Альтернативы сопоставлены по сохранности, доступности, задержке и стоимости; скрытая общая зависимость названа; настройки engine не заменяют системный аргумент. |

<a id="plan-shard-ownership-transfer"></a>

## `b5.capability.plan-shard-ownership-transfer` — Определять безопасный перенос владения шардами

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.plan-shard-ownership-transfer-l1-explain-history` | L1 | Объясняет историю запроса во время переноса шарда | Различены старый и новый владелец, устаревший маршрут и момент принятия записи; копирование не приравнено к передаче права записи. |
| `b5.level-outcome.plan-shard-ownership-transfer-l2-define-bounded-model` | L2 | Задаёт ограниченный переход владения ключами | Названы ключ разбиения, состояния перехода, источники истины и допустимые чтения/записи на каждом состоянии; обозначено поведение старого маршрута. |
| `b5.level-outcome.plan-shard-ownership-transfer-l3-defend-tradeoff` | L3 | Защищает переход при hot key, паузе и неполной копии | Сравнены варианты ограничения записи и перенаправления; инвариант проверен по историям конкурирующих владельцев; цена движения данных и предел возврата явны. |

<a id="define-delivery-contract"></a>

## `b5.capability.define-delivery-contract` — Определять договор доставки и повторного чтения

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.define-delivery-contract-l1-explain-history` | L1 | Объясняет заданную повторную доставку | Подтверждение брокера, получение потребителем и бизнес-эффект различены; порядок в одной области не распространён на все сообщения. |
| `b5.level-outcome.define-delivery-contract-l2-define-bounded-model` | L2 | Задаёт договор доставки для ограниченного потока | Названы producer, broker/log, consumers, область порядка, retention/replay и граница acknowledgement; указаны допустимые потери и дубликаты. |
| `b5.level-outcome.define-delivery-contract-l3-defend-tradeoff` | L3 | Защищает договор при независимых потребителях и отставании | Сопоставлены очередь и журнал по replay, изоляции и цене удержания; гарантия доставки не названа exactly-once бизнес-эффектом. |

<a id="bound-repeat-effects"></a>

## `b5.capability.bound-repeat-effects` — Ограничивать бизнес-эффекты повторного исполнения

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.bound-repeat-effects-l1-explain-history` | L1 | Объясняет повтор при потерянном ответе | Повтор той же операции отделён от нового намерения; уникальный message ID не выдан за бизнес-идентичность. |
| `b5.level-outcome.bound-repeat-effects-l2-define-bounded-model` | L2 | Задаёт договор повторного эффекта одной операции | Определены ключ и scope, конфликт payload, сохранение результата и повтор после истечения истории; границы эффектов названы отдельно от доставки. |
| `b5.level-outcome.bound-repeat-effects-l3-defend-tradeoff` | L3 | Защищает повтор при рестарте и неатомарном внешнем эффекте | Рассмотрены окна между записью результата и эффектом, повтор после retention и reconciliation; явно названа гарантия, которую нельзя получить локальной дедупликацией. |

<a id="control-retry-propagation"></a>

## `b5.capability.control-retry-propagation` — Ограничивать распространение повторов и poison work

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.control-retry-propagation-l1-explain-history` | L1 | Объясняет каскад повторов по заданной цепочке | Различены временный отказ, неизвестный исход и повторяемая ошибка данных; показано усиление попыток на нескольких границах. |
| `b5.level-outcome.control-retry-propagation-l2-define-bounded-model` | L2 | Задаёт политику повторов ограниченной цепочки | Названы владелец повторов, общий бюджет как принцип, backoff/jitter, условия остановки и изоляции poison work; replay имеет отдельное решение. |
| `b5.level-outcome.control-retry-propagation-l3-defend-tradeoff` | L3 | Защищает политику при перегрузке и неоднозначном результате | Сопоставлены прогресс, повторный эффект и усиление нагрузки; предложены различающие наблюдения и сигнал пересмотра, без произвольных численных thresholds. |

<a id="bound-cache-staleness"></a>

## `b5.capability.bound-cache-staleness` — Определять системную границу устаревания cache

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.bound-cache-staleness-l1-explain-history` | L1 | Объясняет заданное устаревшее чтение через cache | Названы authoritative state, cache и путь обновления; TTL не назван гарантией свежести без временных допущений. |
| `b5.level-outcome.bound-cache-staleness-l2-define-bounded-model` | L2 | Задаёт договор свежести для ограниченного пути чтения | Указаны допустимое устаревание, потеря invalidation, повторное заполнение и поведение при недоступности источника. |
| `b5.level-outcome.bound-cache-staleness-l3-defend-tradeoff` | L3 | Защищает договор при конкурирующих обновлениях и отказе источника | Сопоставлены доступность, свежесть и стоимость обращений; рассмотрены гонка заполнения и массовое истечение, указан предел вывода без наблюдений. |

<a id="control-system-load"></a>

## `b5.capability.control-system-load` — Управлять нагрузкой и деградацией между участниками

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.control-system-load-l1-explain-history` | L1 | Объясняет распространение очереди в заданном потоке | Названы producer, bottleneck и потребители ресурсов; отказ в приёме отличён от молчаливой потери уже принятой работы. |
| `b5.level-outcome.control-system-load-l2-define-bounded-model` | L2 | Задаёт ограниченную модель управления потоком | Названы точки обратного давления, единица квоты, очередь, приоритет и судьба отклонённой работы; глобальная квота отделена от локальной. |
| `b5.level-outcome.control-system-load-l3-defend-tradeoff` | L3 | Защищает деградацию при потере части мощности и burst | Сопоставлены справедливость, полезный throughput и задержка; учтены задержанное обратное давление, retry и cache miss; решение остаётся межсистемным, без API abuse implementation. |

<a id="compose-state-and-publication"></a>

## `b5.capability.compose-state-and-publication` — Согласовывать фиксацию состояния и публикацию

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.compose-state-and-publication-l1-explain-history` | L1 | Объясняет разрыв между commit и публикацией | Локальная атомарность отделена от доставки и применения; потерянное подтверждение не доказывает потерю события. |
| `b5.level-outcome.compose-state-and-publication-l2-define-bounded-model` | L2 | Задаёт модель согласования одной записи и события | Для прямой отправки, outbox или CDC обозначены границы durable intent, публикации и повторного получения; история включает остановку между границами. |
| `b5.level-outcome.compose-state-and-publication-l3-defend-tradeoff` | L3 | Защищает композицию при независимом отказе store и доставки | Альтернативы сопоставлены по потерям, дубликатам, порядку и цене сопровождения; outbox/CDC не приписана дедупликация эффекта получателя. |

<a id="choose-cross-system-atomicity"></a>

## `b5.capability.choose-cross-system-atomicity` — Выбирать границу атомарности и компенсации

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.choose-cross-system-atomicity-l1-explain-history` | L1 | Объясняет заданное частично выполненное действие | Различены rollback локальной транзакции, отмена намерения и новый компенсирующий эффект; внешнее действие не объявлено стёртым. |
| `b5.level-outcome.choose-cross-system-atomicity-l2-define-bounded-model` | L2 | Описывает состояния ограниченной операции нескольких участников | Названы локальные commits, общее завершение, неизвестные исходы, компенсация и ручное разрешение; схема остаётся моделью, без реализации coordinator. |
| `b5.level-outcome.choose-cross-system-atomicity-l3-defend-tradeoff` | L3 | Защищает выбор при недоступном участнике и необратимом эффекте | Сравнены координация и saga по атомарности, промежуточной видимости, блокированию и цене восстановления; невозможное обещание заменено явной границей гарантии. |

<a id="assess-regional-capacity"></a>

## `b5.capability.assess-regional-capacity` — Оценивать системную ёмкость и региональный компромисс

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.assess-regional-capacity-l1-explain-history` | L1 | Объясняет заданное перемещение нагрузки после отказа региона | Различены номинальная и оставшаяся мощность, locality и межрегиональная связь; наличие второго региона не выдано за готовность failover. |
| `b5.level-outcome.assess-regional-capacity-l2-define-bounded-model` | L2 | Строит модель ёмкости ограниченного регионального сервиса | Названы workload, узкое место, допущения о ресурсе и росте, пути данных и последствия потери региона; неизвестные параметры помечены. |
| `b5.level-outcome.assess-regional-capacity-l3-defend-tradeoff` | L3 | Защищает региональное решение при неопределённом спросе и коррелированном отказе | Сопоставлены стоимость резерва, latency, согласованность и data locality; дана чувствительность к допущениям и граница вывода, без production topology и DR runbook. |

<a id="preserve-mixed-version-contract"></a>

## `b5.capability.preserve-mixed-version-contract` — Сохранять договор при смешанных версиях

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.preserve-mixed-version-contract-l1-explain-history` | L1 | Объясняет заданную историю старого и нового потребителя | Синтаксическая совместимость отличена от изменения бизнес-смысла, replay старого события и сохранённых состояний. |
| `b5.level-outcome.preserve-mixed-version-contract-l2-define-bounded-model` | L2 | Задаёт допустимые сочетания версий ограниченного взаимодействия | Указаны producers/readers, события, состояния, порядок включения нового смысла и граница возврата; B2 API и B3 schema не дублируются. |
| `b5.level-outcome.preserve-mixed-version-contract-l3-defend-tradeoff` | L3 | Защищает эволюцию при длительном отставании и неполном возврате | Сравнены альтернативы периода совместимости и необратимые эффекты; сохранение системного инварианта проверено по смешанным историям, а не только формату сообщения. |

<a id="design-distinguishing-histories"></a>

## `b5.capability.design-distinguishing-histories` — Проектировать различающие проверки системной гарантии

| ID | Level | Действие и контекст | Evidence criteria |
|---|---|---|---|
| `b5.level-outcome.design-distinguishing-histories-l1-explain-history` | L1 | Объясняет вывод из заданной истории отказа | Отсутствие ошибки отделено от подтверждения инварианта; неполный след отмечен как недостаточный для вывода. |
| `b5.level-outcome.design-distinguishing-histories-l2-define-bounded-model` | L2 | Строит ограниченный набор различающих историй | Для заявленной гарантии заданы участники, причинный порядок, наблюдаемые состояния и критерии трёх исходов; контроль отличает дефект механизма от дефекта наблюдения. |
| `b5.level-outcome.design-distinguishing-histories-l3-defend-tradeoff` | L3 | Защищает достаточность проверки при ограниченной наблюдаемости | Сопоставлены альтернативные причины, вмешательство в timing и цена дополнительных следов; названы непроверенные исполнения, лабораторный результат не объявлен production evidence. |

## Применимость уровней

51 outcome: L1 — 17, L2 — 17, L3 — 17, L4 — 0, L5 — 0. Для каждого действия различены объяснение, самостоятельная модель и защита компромисса. L4/L5 не заданы: в scope отсутствуют отдельные результаты реального adoption/migration нескольких команд и организационного исполнения. Сложная модель, design document и лаборатория не заменяют их. Навигационные L4/L5 из RoleViews не наследуются строками. Отсутствие уровня не означает нулевую способность.
