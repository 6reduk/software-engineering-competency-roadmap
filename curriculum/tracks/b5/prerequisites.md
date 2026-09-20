---
artifact: b5-prerequisites-blueprint
title: "Зависимости и входные условия B5"
owner_track: b5
status: accepted
updated: 2026-09-17
language: ru
---

# Зависимости и входные условия B5

[Формат](README.md#notation) разделяет необходимые способности, полезную последовательность и доступность среды. Полного завершения соседних вертикалей не требуется.

<a id="baseline"></a>

## Внешний hard baseline и conditional concepts

| Основание | Необходимое понятие и действие | Где применяется |
|---|---|---|
| Hard [A1](../catalog/a1-computer-science.md) | Инвариант и контрпример, граф и частичный порядок, конкуренция процессов, оценка стоимости работы; уметь отличить правило безопасности от условия продолжения | Все модули; порядок особенно нужен TO01, оценка стоимости CM01/LC01 |
| Hard [A3](../catalog/a3-networks-linux-security.md) | Путь запроса, соединение, потеря ответа, пауза процесса и ресурсный предел, базовая граница доверия; отличать транспортный симптом от результата приложения | Все модули; независимость сети и участников входит в модель, не в реализацию протокола |
| Conditional [B2](../catalog/b2-backend-api.md) | Контракт ответа/ошибки для FM01/CA01; идентичность прикладной операции и integration acknowledgement для ME01/IR01/DT01; cache boundary для LC01; смысл контракта reader/writer для EV01 | Только если соответствующий service/API участвует в выбранной истории; локальная интеграция остаётся B2 |
| Conditional [B3](../catalog/b3-transactional-data.md) | Commit/rollback, локальная атомарность и сохранность записи для FM01/IR01/DT01; видимость реплики для CA01/RS01; совместимость сохранённых данных для EV01 | Только истории с persistence; наличие SE01 или другой B3 работы не доказывает владение понятиями |

Это текстовая входная спецификация со ссылками на реальные каталоги, без фиктивных внешних capability edges и без порогов подготовки человека. Полный A1/A3 курс не назначается; полное завершение B2/B3 и их module gates не prerequisites. В исходных каталогах нет evidence конкретного участника; оно здесь не изобретается.

<a id="hard-dag"></a>

## Internal Requires

Направление записи: зависимая capability → необходимая capability. Ребро не требует завершить модуль или все уровни prerequisite.

| Capability | Requires | Необходимость |
|---|---|---|
| `b5.capability.choose-read-guarantees` | `b5.capability.model-partial-failures` | Чтобы определить ответ при недоступности узла, необходимо различить недоступность связи, неизвестную запись и отказ участника; иначе договор чтения не имеет определённой области отказов. |
| `b5.capability.exclude-stale-actors` | `b5.capability.reconstruct-causal-order` | Исключение старого действия требует отличать выдачу новых полномочий от причинно предшествующего действия старого владельца; одного времени на часах недостаточно. |
| `b5.capability.compose-state-and-publication` | `b5.capability.define-delivery-contract` | Композиция commit и публикации требует определить, что означает подтверждение доставки и её повтор; без этого системная гарантия не сформулирована. |
| `b5.capability.choose-cross-system-atomicity` | `b5.capability.model-partial-failures` | Выбор общего завершения или компенсации требует различать известный отказ и неизвестный эффект другого участника. |
| `b5.capability.plan-shard-ownership-transfer` | `b5.capability.choose-state-placement` | Передача права записи опирается на определённую модель владельцев, копий и подтверждения; иначе нельзя указать сохраняемый договор данных. |

Оценка границ согласования и смены лидера (`b5.capability.assess-leadership-guarantees`) рассматривает уже заданную ограниченную модель согласования и получает предположения об отказах участников как вход. Самостоятельно строить модель частичных отказов (`b5.capability.model-partial-failures`) полезно, но для этого ограниченного действия не необходимо, поэтому hard edge между ними не задан. Это сохраняет обязательную базу A1/A3 и не мешает будущему slice потребовать конкретную готовность к работе (readiness).

Все 17 узлов разрешаются в [capabilities](capabilities.md). Пять рёбер образуют ацикличный граф: их пять зависимых узлов не являются prerequisites других рёбер. Один допустимый порядок (prerequisite раньше зависимого):

`b5.capability.model-partial-failures`; `b5.capability.reconstruct-causal-order`; `b5.capability.assess-leadership-guarantees`; `b5.capability.choose-state-placement`; `b5.capability.define-delivery-contract`; `b5.capability.bound-repeat-effects`; `b5.capability.control-retry-propagation`; `b5.capability.bound-cache-staleness`; `b5.capability.control-system-load`; `b5.capability.assess-regional-capacity`; `b5.capability.preserve-mixed-version-contract`; `b5.capability.design-distinguishing-histories`; `b5.capability.choose-read-guarantees`; `b5.capability.exclude-stale-actors`; `b5.capability.compose-state-and-publication`; `b5.capability.choose-cross-system-atomicity`; `b5.capability.plan-shard-ownership-transfer`.

У остальных узлов нет internal Requires. Это не запрет полезного порядка и не глобальный DAG всех треков.

<a id="related"></a>

## Related

Направленные навигационные `relates-to`, без обязательного порядка и без включения в hard DAG.

| Capability | Related | Почему не hard |
|---|---|---|
| `b5.capability.assess-leadership-guarantees` | `b5.capability.exclude-stale-actors` | Leadership помогает обсуждать authority, но модель agreement можно оценить без проектирования внешнего fencing; election сама не гарантирует исключение старого эффекта. |
| `b5.capability.choose-state-placement` | `b5.capability.choose-read-guarantees` | Placement влияет на чтения, но ограниченную модель копий можно строить при уже заданном договоре видимости. |
| `b5.capability.bound-repeat-effects` | `b5.capability.define-delivery-contract` | Дубликаты доставки дают контекст; идентичность эффекта можно определить и для повторного прямого вызова. |
| `b5.capability.control-retry-propagation` | `b5.capability.control-system-load` | Retry усиливает нагрузку, однако ограниченную политику повторов можно задать при готовой модели ресурсов. |
| `b5.capability.bound-cache-staleness` | `b5.capability.choose-read-guarantees` | Свежесть cache уточняет договор чтения, но начальное действие возможно при заданной гарантии без выбора общей consistency model. |
| `b5.capability.assess-regional-capacity` | `b5.capability.choose-state-placement` | Placement уточняет цену регионального пути, но capacity-модель может принимать размещение как входное условие. |
| `b5.capability.preserve-mixed-version-contract` | `b5.capability.define-delivery-contract` | Replay влияет на совместимость; синхронное взаимодействие не требует предварительного проектирования потока событий. |
| `b5.capability.design-distinguishing-histories` | `b5.capability.model-partial-failures` | Проверка пользуется моделью отказов, но её можно проектировать для уже заданных failures и гарантии; самостоятельное построение модели не универсальный prerequisite. |

<a id="readiness"></a>

## Future readiness questions

Доступность среды, версии и runtime-семантика **не проверены**. Это вопросы будущего отдельно назначенного пакета после выбора slice, а не hard capability edges и не проведённый Gate 0.

| Контекст | Что потребуется выяснить | Кто уточняет в будущем и каким способом |
|---|---|---|
| Доставка и эффект: ME01/IR01/DT01 | Видны ли durable intent, подтверждения, рестарты и фактический эффект как связанные наблюдения? Каковы реальные retention/replay и crash semantics выбранных компонентов? | Автор будущего slice через первичную документацию выбранных версий и изолированную проверку различающих историй |
| Authority: TO01/CL01 | Можно ли независимо приостановить старого исполнителя, сменить полномочия и наблюдать принятие/отклонение эффекта у ресурса? Где действительно проверяется epoch/lease? | Автор будущего slice совместно с владельцем тестовой среды проверяет доступы и управляемость событий |
| Чтения/placement: CA01/RS01/CM01 | Доступны ли состояния копий, маршруты и причинные следы при отставании; соответствует ли модель независимости отказов среде? | Автор будущего slice проверяет инструментальные границы; облачные регионы не обязательны автоматически |
| Свежесть, нагрузка и изменение: LC01/EV01 | Различимы ли очередь и потеря работы, cache miss и недоступность источника, старый смысл и старый формат? Не искажает ли сбор следов порядок? | Автор будущего slice определяет наблюдения и контроль после отдельного назначения |

Если необходимое наблюдение требует выхода за bounded scope, останавливается зависимый slice и передаётся точный пробел оркестратору. Документальная карта от этого не получает фиктивного runtime blocker. B6 отвечает за реализацию среды, B7 — за эксплуатационный допуск; ни одна будущая проверка автоматически их не заменяет.
