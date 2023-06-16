from core.helpers.admin import user_admin_site
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


@register(UserProfile, site=user_admin_site)
class UserProfileAdmin(UserAdmin):
    model = UserProfile

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserProfile]:
        queryset = super().get_queryset(request)
        if not request.user.is_staff:
            queryset = queryset.filter(pk=request.user.pk)
        return queryset

    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_staff:
            return False
        return super().has_add_permission(request)

    def has_view_permission(self, request: HttpRequest, obj: UserProfile = None) -> bool:
        if not request.user.is_staff:
            if obj:
                return obj == request.user
            return True
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request: HttpRequest, obj: UserProfile = None) -> bool:
        if not request.user.is_staff:
            if obj:
                return obj == request.user
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request: HttpRequest, obj: UserProfile = None) -> bool:
        if not request.user.is_staff:
            return False
        return super().has_delete_permission(request, obj)

    def has_module_permission(self, request: HttpRequest) -> bool:
        return True
