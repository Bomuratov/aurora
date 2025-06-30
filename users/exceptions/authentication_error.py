from rest_framework.exceptions import APIException

class AuthenticationErrorException(APIException):
    status_code = 401
    default_detail = "Токен недействителен или просрочен"
    default_code = "authentication error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        self.detail = {"message": detail, "code": code}