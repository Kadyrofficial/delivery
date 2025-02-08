from rest_framework import viewsets, filters
from .models import User, Code
from .serializers import UserLessDetailSerializer, UserSerializer, AuthSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(type__in=['customer', 'client', 'delivery'])
    serializer_class = UserLessDetailSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type']
    search_fields = ['title_tm', 'title_ru']


class AuthViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, lang, *args, **kwargs):
        queryset = User.objects.get(id=self.request.user.id)
        serializer = UserLessDetailSerializer(queryset, context={'lang': lang, "request": request})
        return Response(serializer.data)
    
    def retrieve(self, request,  lang, *args, **kwargs):
        instance = User.objects.get(id=self.request.user.id)
        serializer = self.get_serializer(instance, context={'lang': lang, "request": request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = User.objects.get(id=self.request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        password = request.data.get('password')
        forgot_password = request.data.get('forgot_password')

        if serializer.is_valid():
            if email and phone_number:
                return Response({'message': 'Send phone_number or email, not both'}, status=status.HTTP_400_BAD_REQUEST)

            if email:
                user = User.objects.filter(email=email).first()

                if code:
                    if not user:
                        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                    code_instance = Code.objects.filter(user=user, code=code).first()
                    if code_instance:
                        if code_instance.is_valid():
                            if password:
                                if forgot_password:
                                    return Response({'message': 'Invalid logic with forgot_password and password together'}, status=status.HTTP_400_BAD_REQUEST)
                                user.set_password(password)
                                user.save()
                                user = authenticate(email=email, password=password)
                                if user:
                                    refresh = RefreshToken.for_user(user)
                                    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
                                return Response({'message': 'Authentication failed after password reset'}, status=status.HTTP_400_BAD_REQUEST)
                            return Response({'code': code}, status=status.HTTP_200_OK)
                        return Response({'message': 'Code is expired'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'message': 'Code not found'}, status=status.HTTP_404_NOT_FOUND)

                if password:
                    if forgot_password:
                        return Response({'message': 'Invalid logic with forgot_password and password together'}, status=status.HTTP_400_BAD_REQUEST)
                    if user and user.check_password(password):
                        refresh = RefreshToken.for_user(user)
                        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
                    return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

                if forgot_password:
                    if user:
                        code = get_random_string(length=6, allowed_chars='0123456789')
                        send_mail(
                            subject='Your OTP Code',
                            message=f'Your OTP code is {code}',
                            from_email='your_email@example.com',
                            recipient_list=[email],
                            fail_silently=False,
                        )
                        Code.objects.create(user=user, code=code)
                        return Response({'email': email}, status=status.HTTP_200_OK)
                    return Response({'message': 'Email not found. Please register'}, status=status.HTTP_404_NOT_FOUND)

                if user:
                    return Response({'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

                code = get_random_string(length=6, allowed_chars='0123456789')
                user = User.objects.create(email=email)
                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP code is {code}',
                    from_email='your_email@example.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                Code.objects.create(user=user, code=code)
                return Response({'email': email}, status=status.HTTP_200_OK)

            return Response({'message': 'Please provide an email or phone number'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.action == "update":
            return User.objects.get(id=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return AuthSerializer
        if self.action == "update":
            return UserSerializer
        return super().get_serializer_class()
