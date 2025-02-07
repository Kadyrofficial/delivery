from rest_framework import viewsets, filters
from .models import User
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsCustomerUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.customers.get(id=self.request.user.id)
    permission_classes = [IsCustomerUser]

    
    # def get_serializer_class(self):
    #     if self.action == "list":
    #         return ProductListSerializer
    #     if self.action == "retrieve":
    #         return ProductRetrieveSerializer
    #     return super().get_serializer_class()
