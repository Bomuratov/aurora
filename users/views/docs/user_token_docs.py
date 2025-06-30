from types import SimpleNamespace

docs = SimpleNamespace(
    tags=["USER LOGIN NATIVE API v1.01"],
    description=SimpleNamespace(
        access="""
        USER LOGIN NATIVE 'POST' данный API для входа в сервис API ожиданет два поля phone и password b возврашает access и refresh токены
        """,
        refresh="""
        USER LOGIN NATIVE 'POST' данный API нужен чтобы взять новый access токен API ожидает старый refresh токен.
        """,
    )
)

web_docs = SimpleNamespace(
    tags=["USER LOGIN WEB API v1.01"],
    description=SimpleNamespace(
        access="""
        USER LOGIN WEB 'POST' данный API предназначен для логина пользователей в response возврашается access токен, срок жизни access токена (в формате unix),
        срок жизни refresh токена (в формате unix) и в куках самостоятельно устанавливает refresh токен session_id и csrft_token.
        """,
        refresh="""
        USER LOGIN NATIVE 'POST' данный API предназначен для получения нового access токена API ожидает refresh токен и в ответ возврашает access токен, 
        срок жизни access токена (в формате unix), срок жизни нового refresh токена (в формате unix) и в куках самостоятельно устанавливает новый refresh токен.
        """,
    )
)