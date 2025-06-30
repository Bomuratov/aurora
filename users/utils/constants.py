
SUPERVISOR = "is_supervisor"
MANAGER = "is_manager"
DIRECTOR = "is_director"
ANALYTIC = "is_analytic"
HR = "is_hr"
AGENT = "is_agent"
COURIER = "is_courier"
DISPATCHER = "is_dispatcher"
OPERATOR = "is_operator"
WAITER = "is_waiter"
SUPER_WAITER = "is_super_waiter"


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
    (WAITER, "Официант"),
    (SUPER_WAITER, "Старший официант"),
)


PERMISSIONS = (
    (ADD, "Доступ добавить"),
    (UPDATE, "Доступ обновить"),
    (DELETE, "Доступ удалить"),
    (VIEW, "Доступ на просмотр"),
)