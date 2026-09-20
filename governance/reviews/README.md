# Reviews: исторический audit trail

Этот каталог хранит отчёты независимых проверок, консолидации и acceptance по
конкретным snapshot. Отчёт фиксирует известное reviewer на момент проверки и
может содержать промежуточный `status: review`, закрытый finding, отменённое
предложение или название использованной модели.

Отчёты не являются текущим source of truth. Актуальное состояние загружается из
[`current-state.yaml`](../state/current-state.yaml), а принятые решения — из
[`decisions.md`](../decisions.md). Reviewer verdict сам по себе не означает
program acceptance, module closure, learner execution или proficiency.

Каталог публикуется для traceability. Редактировать старый report следует только
для исправления доказуемой ошибки с сохранением provenance; новое состояние
обычно оформляется отдельным решением.
