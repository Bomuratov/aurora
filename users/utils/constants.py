
SUPERVISOR = "is_supervisor"
MANAGER = "is_manager"
DIRECTOR = "is_director"
ANALYTIC = "is_analytic"
HR = "is_hr"
AGENT = "is_agent"
COURIER = "is_courier"
DISPATCHER = "is_dispatcher"
OPERATOR = "is_operator"


ADD = "can_add"
UPDATE = "can_update"
DELETE = "can_delete"
VIEW = "can_view"


ROLES = (
    (SUPERVISOR, "Супервайзер"),
    (MANAGER, "Менеджер"),
    (DIRECTOR, "Директор"),
    (ANALYTIC, "Аналитик"),
    (HR, "HR"),
    (AGENT, "Агент"),
    (COURIER, "Курьер"),
    (DISPATCHER, "Диспетчер"),
    (OPERATOR, "Оператор"),
)


PERMISSIONS = (
    (ADD, "Доступ добавить"),
    (UPDATE, "Доступ обновить"),
    (DELETE, "Доступ удалить"),
    (VIEW, "Доступ на просмотр"),
)