class SecurityMiddleware:
    # Token estático de simulación profesional
    ADMIN_TOKEN = "Bearer ADSO-SECURE-TOKEN-2026"

    @staticmethod
    def is_authorized(headers):
        auth_header = headers.get("Authorization")
        if not auth_header or auth_header != SecurityMiddleware.ADMIN_TOKEN:
            return False
        return True
