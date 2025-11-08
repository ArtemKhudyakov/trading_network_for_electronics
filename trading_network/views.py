from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode, Product
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateSerializer,
    ProductSerializer
)
from .filters import NetworkNodeFilter
from users.permissions import CanManageOrganization, IsInSameOrganization

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsActiveEmployeePermission(IsAuthenticated):
    """Разрешение только для активных сотрудников"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_active


# NetworkNode Views
class NetworkNodeListCreateView(generics.ListCreateAPIView):
    """
    get:
    Получить список всех звеньев торговой сети

    **Фильтрация:**
    - `?country=Россия` - по стране
    - `?city=Москва` - по городу
    - `?level=0` - по уровню иерархии
    - `?search=завод` - поиск по названию, стране, городу

    **Сортировка:**
    - `?ordering=created_at` - по дате создания
    - `?ordering=debt` - по задолженности
    - `?ordering=name` - по названию

    post:
    Создать новое звено торговой сети

    **Поля:**
    - `name` (обязательно) - Название звена
    - `level` (обязательно) - Уровень иерархии (0-2)
    - `email` (обязательно) - Email
    - `country`, `city`, `street`, `house_number` - адрес
    - `supplier` - ID поставщика (опционально)
    - `products` - список ID продуктов

    **Примечание:** Поле `debt` нельзя установить при создании
    """

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
        queryset = super().get_queryset()

        if self.request.user.is_staff or self.request.user.role == "manager":
            return queryset

        user_organization = getattr(self.request.user, 'organization', None)
        if user_organization:
            return queryset.filter(id=user_organization.id)

        return queryset.none()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'country',
                openapi.IN_QUERY,
                description="Фильтр по стране",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'city',
                openapi.IN_QUERY,
                description="Фильтр по городу",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'level',
                openapi.IN_QUERY,
                description="Фильтр по уровню иерархии (0-2)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Поиск по названию, стране, городу",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Сортировка (created_at, debt, name)",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class NetworkNodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Получить детальную информацию о звене сети

    **Включает:**
    - Основную информацию
    - Список продуктов
    - Информацию о поставщике
    - Список сотрудников

    put:
    Полностью обновить информацию о звене

    patch:
    Частично обновить информацию о звене

    **Ограничения:**
    - Поле `debt` нельзя изменить через API
    - Обычные пользователи могут редактировать только свою организацию

    delete:
    Удалить звено сети

    **Требуются права менеджера или администратора**
    """

    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization, IsInSameOrganization]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return NetworkNodeCreateSerializer
        return NetworkNodeSerializer

    def update(self, request, *args, **kwargs):
        if 'debt' in request.data:
            request.data.pop('debt')
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff or self.request.user.role == "manager":
            return queryset

        user_organization = getattr(self.request.user, 'organization', None)
        if user_organization:
            return queryset.filter(id=user_organization.id)

        return queryset.none()


# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    """
    get:
    Получить список всех продуктов

    **Поиск и сортировка:**
    - `?search=iphone` - поиск по названию и модели
    - `?ordering=release_date` - по дате выпуска
    - `?ordering=name` - по названию

    post:
    Создать новый продукт

    **Поля:**
    - `name` (обязательно) - Название продукта
    - `model` (обязательно) - Модель
    - `release_date` (обязательно) - Дата выхода на рынок (YYYY-MM-DD)
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'model']
    ordering_fields = ['release_date', 'name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Поиск по названию и модели продукта",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Сортировка (release_date, name)",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Получить детальную информацию о продукте

    put:
    Полностью обновить информацию о продукте

    patch:
    Частично обновить информацию о продукте

    delete:
    Удалить продукт

    **Требуются права менеджера или администратора**
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployeePermission, CanManageOrganization, IsInSameOrganization]