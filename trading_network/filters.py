import django_filters
from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    product_name = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')

    class Meta:
        model = NetworkNode
        fields = ['level', 'country', 'city']