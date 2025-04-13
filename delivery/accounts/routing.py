from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/otp/$', consumers.OTPConsumer.as_asgi()),
]
