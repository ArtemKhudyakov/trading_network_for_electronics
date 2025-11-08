from rest_framework import serializers
from .models import Product, NetworkNode
from users.models import User


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продуктов
    """

    class Meta:
        model = Product
        fields = '__all__'

    def validate_release_date(self, value):
        """
        Проверка что дата выпуска не в будущем
        """
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата выпуска не может быть в будущем")
        return value


class NetworkNodeEmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения сотрудников организации"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения звеньев сети

    Включает расширенную информацию:
    - Детали продуктов
    - Информацию о поставщике
    - Список сотрудников
    """
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    employees = NetworkNodeEmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'level', 'level_display', 'email', 'country', 'city',
            'street', 'house_number', 'products', 'supplier', 'supplier_name',
            'debt', 'created_at', 'employees'
        ]
        read_only_fields = ['debt', 'created_at', 'level_display', 'employees']


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления звеньев сети
    """

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'level', 'email', 'country', 'city',
            'street', 'house_number', 'products', 'supplier',
            'debt', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at']

    def validate_level(self, value):
        """
        Проверка корректности уровня иерархии
        """
        if value not in [0, 1, 2]:
            raise serializers.ValidationError("Уровень должен быть 0, 1 или 2")
        return value

    def validate_supplier(self, value):
        """
        Проверка что поставщик существует и не создает циклических ссылок
        """
        if value and value.level == 2:
            raise serializers.ValidationError("Индивидуальный предприниматель не может быть поставщиком")
        return value