from types import SimpleNamespace

docs = SimpleNamespace(
    tags=["Variant API v1.01"],
    description=SimpleNamespace(
        get_list="Получить список всех вариантов. Фильтрация по полю menu_id нужно передать ID нужной позиции чтобы взять его варианты. API возврашает МАССИВ ОБЪЕКТОВ",
        get_retrieve="Получить один пункт варианта по его ID. API возврашает один объект (DICT, OBJECT) варианта",
        create="Создать новый пункт меню. API возврашает один объект (DICT, OBJECT) варианта",
        update="Полное обновление пункта меню (PUT).API возврашает один объект (DICT, OBJECT) варианта",
        destroy="Удаление пункта меню по ID. API возврашает 204 NO CONTENT ответ "
    )
)