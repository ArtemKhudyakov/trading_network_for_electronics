from rest_framework import permissions


class CanEditUserProfile(permissions.BasePermission):
    """
    Разрешение для редактирования профиля:
    - Владелец может редактировать свой профиль
    - Менеджер может редактировать любой профиль
    """

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True

        user_role = getattr(request.user, "role", None)
        is_manager = user_role == "manager"
        is_admin = request.user.is_staff

        return is_manager or is_admin


class CanViewUserList(permissions.BasePermission):
    """
    Разрешение для просмотра списка пользователей:
    - Только менеджеры и админы
    """

    def has_permission(self, request, view):
        is_manager = request.user.role == "manager"
        is_admin = request.user.is_staff
        return is_manager or is_admin


class IsInSameOrganization(permissions.BasePermission):
    """
    Пользователь может работать только с объектами своей организации
    """

    def has_object_permission(self, request, view, obj):
        # Суперпользователи и менеджеры имеют доступ ко всем организациям
        if request.user.is_staff or request.user.role == "manager":
            return True

        # Проверяем, что объект принадлежит той же организации, что и пользователь
        user_organization = getattr(request.user, 'organization', None)
        obj_organization = getattr(obj, 'organization', None)

        # Если у объекта есть организация, проверяем совпадение
        if obj_organization:
            return user_organization == obj_organization

        # Если у объекта нет организации, доступ только у менеджеров/админов
        return False


class CanManageOrganization(permissions.BasePermission):
    """
    Пользователь может управлять объектами своей организации
    """

    def has_permission(self, request, view):
        # Суперпользователи и менеджеры имеют доступ ко всем организациям
        if request.user.is_staff or request.user.role == "manager":
            return True

        # Обычные пользователи должны иметь организацию
        return request.user.organization is not None

    def has_object_permission(self, request, view, obj):
        # Суперпользователи и менеджеры имеют доступ ко всем организациям
        if request.user.is_staff or request.user.role == "manager":
            return True

        # Проверяем, что объект принадлежит организации пользователя
        user_organization = getattr(request.user, 'organization', None)
        obj_organization = getattr(obj, 'organization', None)

        return user_organization == obj_organization