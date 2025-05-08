from types import SimpleNamespace

docs = SimpleNamespace(
    tags=["Menu API v1.01"],
    description=SimpleNamespace(
        get_list="Получить список всех пунктов меню. Можно фильтровать по restaurant__name и category_id.",
        get_retrieve="Получить один пункт меню по ID.",
        create="Создать новый пункт меню.",
        update="Полное обновление пункта меню (PUT).",
        partial_update="Частичное обновление пункта меню (PATCH).",
        destroy="Удаление пункта меню по ID."
    )
)