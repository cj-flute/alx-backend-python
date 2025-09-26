# chats/auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend JWTAuthentication if you want custom behavior.
    Example: allow JWT in query params or a custom header.
    """

    def authenticate(self, request):
        # Example: accept JWT from ?token=... in query string
        token = request.query_params.get("token")
        if token:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return (user, validated_token)

        # fallback to normal JWT behavior
        return super().authenticate(request)
