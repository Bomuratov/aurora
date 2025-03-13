
SUPERVISOR = "is_supervisor"
MANAGER = "is_manager"
DIRECTOR = "is_director"
ANALYTIC = "is_analytic"
HR = "is_hr"
AGENT = "is_agent"
OWNER = "is_owner"
SUPERADMIN = "is_superadmin"

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
    (OWNER, "Создатель"),
    (SUPERADMIN, "Super admin"),
)

PERMISSIONS = (
    (ADD, "Доступ добавить"),
    (UPDATE, "Доступ обновить"),
    (DELETE, "Доступ удалить"),
    (VIEW, "Доступ на просмотр"),
)