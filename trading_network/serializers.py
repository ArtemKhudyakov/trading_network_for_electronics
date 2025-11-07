from rest_framework import serializers
from .models import Product, NetworkNode


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'level', 'level_display', 'email', 'country', 'city',
            'street', 'house_number', 'products', 'supplier', 'supplier_name',
            'debt', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at', 'level_display']


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'level', 'email', 'country', 'city',
            'street', 'house_number', 'products', 'supplier',
            'debt', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at']