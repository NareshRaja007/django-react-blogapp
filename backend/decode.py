import jwt
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_webapp.settings")
django.setup()

from django.conf import settings

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjY1MzI1LCJpYXQiOjE3NDI2NjM1MjUsImp0aSI6IjA0YWRhNjg2Y2ZjYzQwOGNiNTk1OTkyNjU3ZDFkMzk5IiwidXNlcl9pZCI6InJhajAwNyJ9.j3k92RRWlMLjskOgiu0oIpxe-Fa2JIhmgNVSzqCLDas"  # Replace with actual token from Postman

try:
    decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    print("Decoded JWT Payload:", decoded_payload)

    if "user_id" not in decoded_payload:
        print("❌ ERROR: 'user_id' is missing from JWT payload!")
    else:
        print("✅ SUCCESS: 'user_id' is present in JWT payload.")

except jwt.ExpiredSignatureError:
    print("❌ ERROR: Token has expired!")
except jwt.InvalidTokenError:
    print("❌ ERROR: Invalid token!")
