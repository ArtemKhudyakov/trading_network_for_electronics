from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Схема для Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="ElectroHub Trade Network API",
        default_version='v1',
        description="""
        **ElectroHub - API для управления торговой сетью электроники**

        ### Основные возможности:
        - Управление иерархической структурой сети (Заводы → Розничные сети → ИП)
        - Управление продуктами и каталогом
        - Управление пользователями и правами доступа
        - JWT аутентификация

        ### Уровни иерархии:
        - **0** - Завод
        - **1** - Розничная сеть  
        - **2** - Индивидуальный предприниматель

        ### Аутентификация:
        Все запросы требуют JWT токена, кроме:
        - `/users/api/login/` - получение токена
        - `/users/api/register/` - регистрация
        - `/users/api/token/refresh/` - обновление токена

        ### Права доступа:
        - **Обычные пользователи** - доступ только к своей организации
        - **Менеджеры** - полный доступ ко всем организациям
        - **Администраторы** - полный доступ + админ-панель
        """,
        terms_of_service="https://www.electrohub.ru/terms/",
        contact=openapi.Contact(email="api@electrohub.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("", TemplateView.as_view(template_name="home.html"), name="home"),
                  path("users/", include("users.urls", namespace="users")),
                  path("trading/", include("trading_network.urls")),
                  path("api-docs/", TemplateView.as_view(template_name="api_docs.html"), name="api_docs"),

                  # ✅ URLs для документации API
                  path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)