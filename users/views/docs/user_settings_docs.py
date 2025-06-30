from types import SimpleNamespace

docs = SimpleNamespace(
    tags=["USER SETTINGS API v1.01"],
    description=SimpleNamespace(
        list="""
        USER SETTINGS 'GET' данный API позволяет получить все существующие FCM_TOKEN ы пользователей .
        """,
        update="""
        USER SETTINGS 'PUT' данный API предназначен чтобы изменить или обновить FCM_TOKEN ы пользователя.

        API ожидает что вы передадите индентификатор (ID) пользователя (user_id).
        """,
    )
)
