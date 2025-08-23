from django.core.validators import RegexValidator

UZB_PHONE_VALIDATOR = RegexValidator(regex=r"^(\+998)(\d{9})$", message="Введённый номер телефона неправильно. Пример +998(XX)XXX-XX-XX")
INTERNATIONAL_PHONE_VALIDATOR = RegexValidator(regex=r"^(\+)(\d{12})$", message="Номер в международном формате начинается с +")
