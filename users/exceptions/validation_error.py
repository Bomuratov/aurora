from rest_framework.exceptions import APIException

class ValidateErrorException(APIException):
    status_code = 400
    default_detail = "Ошибка валидации"
    default_code = "validation_error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        self.detail = {"message": detail, "code": code}