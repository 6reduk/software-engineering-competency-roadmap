---
id: b2.index.service-architecture-boundaries
kind: index
title: Service Architecture — изоляция изменения бизнес-политики
owner_track: b2
module: b2.module.service-architecture
coverage:
  - target: b2.capability.design-service-architecture
    role: reference
  - target: b2.capability.verify-service-behavior
    role: reference
status: accepted
updated: 2026-08-19
language: ru
---

# Service Architecture: изоляция изменения бизнес-политики

В Orders service операция `GET /orders/{order_id}/cancellation-eligibility` отвечает, можно ли отменить заказ. Пока отменять можно было только `CREATED`, router сам загружал ORM-модель, проверял статус, вызывал Carrier API и формировал HTTP-ответ. Новое правило разрешает клиенту `PREMIUM` отменить и `PACKED`, если перевозчик ещё не начал передачу. Теперь одна правка затрагивает router, ORM, HTTP client и тесты, привязанные к их внутренностям.

Этот slice учит не «идеальной чистой архитектуре», а управляемости следующего изменения: отделить чистое бизнес-решение от координации операции и от способов доставки, хранения и сетевого вызова; затем доказать эффект тестами и заменой адаптера. Количество слоёв, классов и интерфейсов не считается результатом.

## Кому и что потребуется

Материал полезен инженеру, который уверенно меняет endpoint, но сталкивается с растущей ценой согласованных правок. Нужны базовые навыки Python и тест-дизайна, понимание HTTP request/response boundary и умение читать небольшой FastAPI-сервис. Фактическая HTTP-граница уже разобрана в [материале об исполнении контракта](../evolvable-api-contracts/learn/http-contract-execution-boundary.md), а lifecycle и ограничения downstream client — в [материале о насыщении пула](../runtime-concurrency-lifecycle/learn/bounded-concurrency-pool-saturation.md). Здесь они используются как готовые границы, а не объясняются заново.

## Маршрут

1. [Brief](learn/change-isolation-service-boundaries.md) — найти связанность по пути изменения, выбрать минимальные границы и спланировать постепенный переход.
2. [Interview](interview/service-boundary-change.md) — проговорить диагностику, альтернативы, migration plan и доказательства уровня L1–L3.
3. [Kata](kata/extract-order-cancellation-policy.md) — самостоятельно собрать намеренно связанный scaffold и провести изменение без готового решения.
4. [Project specification](project-spec/order-cancellation-policy-service.md) — интегрировать выбранную границу с реальными persistence и HTTP adapters и проверить повторное изменение.

После маршрута инженер должен уметь сохранить заданную границу в локальной правке, самостоятельно разместить типовую feature между application/domain/adapters и перестроить накопившую связанность с зафиксированной исходной болью, альтернативами и наблюдаемым уменьшением поверхности изменения.

## Границы пакета

Операция только вычисляет eligibility: она не пишет в БД, не делает refund, не публикует событие и не создаёт удалённый side effect. Transaction, unit of work, outbox и consistency относятся к будущим пакетам; retry downstream-вызова уже разобран в связанном runtime-материале. Не рассматриваются microservice decomposition, обязательный repository/DI container, полная verification strategy и межкомандные L4 conventions.

Business-policy tests доказывают правило без I/O; отдельные adapter checks доказывают преобразование реальных границ. Fake не доказывает корректность ORM- или HTTP-mapping, а удачный wiring сам по себе не доказывает изоляцию изменения.
