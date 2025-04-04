from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsSuperUser, IsAdminOrSuperUser
from .models import User, Code
from .serializers import UserSerializer, ProfileSerializer, AuthSerializer, LoginSerializer, VerifySerializer


class UserViewSet(viewsets.ModelViewSet):

    @action(methods=['get', 'put'], detail=False, url_path='profile')
    def profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user, context={'request': request})
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = self.get_serializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'get'], detail=False, url_path='auth')
    def auth(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            email = request.data.get('email')
            phone_number = request.data.get('phone_number')
            code = request.data.get('code')

            if serializer.is_valid():
                if email and phone_number:
                    return Response({'message': 'Send phone_number or email, not both'}, status=status.HTTP_400_BAD_REQUEST)
                if email:
                    if code:
                        user = User.objects.filter(email=email).first()
                        if not user:
                            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                        code_instance = Code.objects.filter(user=user, code=code).first()
                        if code_instance.is_valid():
                            try:
                                password = get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                                user.set_password(password)
                                user.save()
                                user = authenticate(email=email, password=password)
                                access_token = RefreshToken.for_user(user).access_token
                                return Response({'access': str(access_token)}, status=status.HTTP_200_OK)
                            except:
                                return Response({'error': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
                        elif not code_instance.is_valid():
                            return Response({'message': 'Code is expired'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'message': 'Code not found'}, status=status.HTTP_404_NOT_FOUND)
                    try:
                        code = get_random_string(length=4, allowed_chars='0123456789')
                        user, created = User.objects.get_or_create(email=email)
                        Code.objects.create(user=user, code=code)
                        send_mail(
                            subject='Your OTP Code',
                            message=f'Your OTP code is {code}',
                            from_email='your_email@example.com',
                            recipient_list=[email],
                            fail_silently=False,
                        )
                        return Response({'email': email}, status=status.HTTP_200_OK)
                    except:
                        return Response({'error': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "GET":
            return Response()


    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')

        if serializer.is_valid():
            try:
                code = get_random_string(length=4, allowed_chars='0123456789')
                user, created = User.objects.get_or_create(email=email)
                Code.objects.create(user=user, code=code)
                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP code is {code}',
                    from_email='your_email@example.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                return Response({'email': email}, status=status.HTTP_200_OK)
            except:
                return Response({'error': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
                
    @action(methods=['post'], detail=False, url_path='verify')
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        code = request.data.get('code')
        user = User.objects.filter(email=email).first()
        if serializer.is_valid:
            if not user:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            code_instance = Code.objects.filter(user=user, code=code).first()
            if code_instance.is_valid():
                try:
                    password = get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    user.set_password(password)
                    user.save()
                    user = authenticate(email=email, password=password)
                    access_token = RefreshToken.for_user(user).access_token
                    return Response({'access': str(access_token)}, status=status.HTTP_200_OK)
                except:
                    return Response({'error': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            elif not code_instance.is_valid():
                return Response({'message': 'Code is expired'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Code not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        if self.request.user.type in [User.UserType.ADMIN]:
            return User.objects.exclude(type = User.UserType.SUPERUSER).order_by('date_joined')
        return User.objects.all().order_by('date_joined')

    def get_permissions(self):
        if self.action == "destroy":
            return [IsSuperUser()]
        if self.action == "login" or "verify":
            return [AllowAny()]
        if self.action == "profile":
            return [IsAuthenticated()]
        return [IsAdminOrSuperUser()]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "profile":
            return ProfileSerializer
        if self.action == "auth":
            return AuthSerializer
        if self.action == "login":
            return LoginSerializer
        if self.action == "verify":
            return VerifySerializer
        return UserSerializer
