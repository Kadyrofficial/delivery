from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Code


User = get_user_model()

class OTPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        email = data.get('email')

        if email:
            code = get_random_string(length=4, allowed_chars='0123456789')
            user, _ = User.objects.get_or_create(email=email)
            Code.objects.create(user=user, code=code)
            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP code is {code}',
                from_email='your_email@example.com',
                recipient_list=[email],
                fail_silently=False,
            )
            await self.send(text_data=json.dumps({
                'email': email,
                'code': code,
                'message': 'OTP sent successfully',
            }))
        else:
            await self.send(text_data=json.dumps({
                'error': 'Email not provided'
            }))
