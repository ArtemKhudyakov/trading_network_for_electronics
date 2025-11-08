from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode, Product
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateSerializer,
    ProductSerializer
)
from .filters import NetworkNodeFilter
from users.permissions import CanManageOrganization, IsInSameOrganization


class IsActiveEmployeePermission(IsAuthenticated):
    """Разрешение только для активных сотрудников"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_active


# NetworkNode Views
class NetworkNodeListCreateView(generics.ListCreateAPIView):
    """Список и создание звеньев сети"""
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NetworkNodeFilter
    search_fields = ['name', 'country', 'city']
    ordering_fields = ['created_at', 'debt', 'name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NetworkNodeCreateSerializer
        return NetworkNodeSerializer

    def get_queryset(self):
        """Фильтруем queryset в зависимости от прав пользователя"""
        queryset = super().get_queryset()

        if self.request.user.is_staff or self.request.user.role == "manager":
            return queryset

        user_organization = getattr(self.request.user, 'organization', None)
        if user_organization:
            return queryset.filter(id=user_organization.id)

        return queryset.none()


class NetworkNodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали, обновление и удаление звена сети"""
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization,
                          IsInSameOrganization]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return NetworkNodeCreateSerializer
        return NetworkNodeSerializer

    def update(self, request, *args, **kwargs):
        # Запрещаем обновление поля debt через API
        if 'debt' in request.data:
            request.data.pop('debt')
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        """Фильтруем queryset в зависимости от прав пользователя"""
        queryset = super().get_queryset()

        if self.request.user.is_staff or self.request.user.role == "manager":
            return queryset

        user_organization = getattr(self.request.user, 'organization', None)
        if user_organization:
            return queryset.filter(id=user_organization.id)

        return queryset.none()


class ProductListCreateView(generics.ListCreateAPIView):
    """Список и создание продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'model']
    ordering_fields = ['release_date', 'name']


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали, обновление и удаление продукта"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization,
                          IsInSameOrganization]