from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from .models import UserDetails  # ✅ Import your UserDetails model

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
            user_id = validated_token.get("user_id")  # ✅ Get user_id from JWT
            if not user_id:
                raise AuthenticationFailed("User ID not found in token.")

            # ✅ Fetch user from UserDetails model
            try:
                user = UserDetails.objects.get(user_id=user_id)
            except UserDetails.DoesNotExist:
                raise AuthenticationFailed("User not found.")

            return (user, validated_token)

        except ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

