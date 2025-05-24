from types import SimpleNamespace

docs = SimpleNamespace(
    tags=["REGISTER API v1.01"],
    description=SimpleNamespace(
        user_post="""
        Register 'POST' данный API предназначен для регистрации обичньного пользователя
        """,
        vendor_post="""
        Register 'POST' данный API предназначен чтобы рестораны могли создать своих сотрудников с ролями. 
        
        При создании сотрудника для него автоматически создается модель UERSETTINGS с пустыми полями.
        
        API ожидает что вы ему передаете идентификатор (ID) ресторана и идентификатор (ID) роля.
        """,
    )
)
