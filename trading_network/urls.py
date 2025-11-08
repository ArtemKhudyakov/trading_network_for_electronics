from django.urls import path
from .views import (
    NetworkNodeListCreateView,
    NetworkNodeDetailView,
    ProductListCreateView,
    ProductDetailView
)

app_name = 'trading_network'

urlpatterns = [
    # NetworkNode URLs
    path('api/network-nodes/', NetworkNodeListCreateView.as_view(), name='network-node-list'),
    path('api/network-nodes/<int:pk>/', NetworkNodeDetailView.as_view(), name='network-node-detail'),

    # Product URLs
    path('api/products/', ProductListCreateView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]