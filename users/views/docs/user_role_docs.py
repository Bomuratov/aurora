from types import SimpleNamespace

docs = SimpleNamespace(
    tags=["USER ROLES API v1.01"],
    description=SimpleNamespace(
        list="""
        USER ROLES 'GET' данный API позволяет получить все существующие роли.
        """,
        create="""
        USER ROLES 'POST' данный API предназначен для создания ролей
        """,
        update="""
        USER ROLES 'PUT' данный API предназначен чтобы изменить или обновить роля.

        API ожидает что вы передадите индентификатор (ID) роля.
        """,
        delete="""
        USER ROLES 'DELETE' данный API предназначен для удаления роля.

        API ожидает что вы передадите индентификатор (ID) роля.
        """,

        get_dict="""
        USER ROLES 'GET' данный API предназначен для получения ключь и название роля.

        Данный API не работает с базой данных.
        """,
    )
)