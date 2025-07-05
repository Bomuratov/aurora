# myapp/middleware.py

import base64
from django.conf import settings
from django.http import HttpResponse


class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/docs/") or request.path.startswith("/schema/"):
            auth_header = request.META.get("HTTP_AUTHORIZATION")
            if auth_header:
                try:
                    auth_type, creds = auth_header.split(" ", 1)
                    if auth_type.lower() == "basic":
                        decoded_creds = base64.b64decode(creds.strip()).decode("utf-8")
                        username, password = decoded_creds.split(":", 1)
                        if username == settings.SWAGGER_USERNAME and password == settings.SWAGGER_PASSWORD:
                            return self.get_response(request)
                except Exception:
                    pass

            response = HttpResponse(status=401)
            response["WWW-Authenticate"] = 'Basic realm="Swagger UI"'
            
            return response

        return self.get_response(request)
