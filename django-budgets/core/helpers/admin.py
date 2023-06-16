from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Model
from django.http import HttpRequest
from django.utils.translation import gettext as _, gettext_lazy


class CustomAdminPermissions(object):

    def has_add_permission(self, request: HttpRequest, obj: Model = None) -> bool:
        if obj:
            default_permission = super().has_view_permission(request, obj)
            if hasattr(obj, 'has_object_permission'):
                return default_permission or obj.has_object_permission(request)
            return default_permission
        return True

    def has_view_permission(self, request: HttpRequest, obj: Model = None) -> bool:
        if obj:
            default_permission = super().has_view_permission(request, obj)
            if hasattr(obj, 'has_object_permission'):
                return default_permission or obj.has_object_permission(request)
            return default_permission
        return True

    def has_change_permission(self, request: HttpRequest, obj: Model = None) -> bool:
        if obj:
            default_permission = super().has_change_permission(request, obj)
            if hasattr(obj, 'has_object_permission'):
                return default_permission or obj.has_object_permission(request)
            return default_permission
        return True

    def has_delete_permission(self, request: HttpRequest, obj: Model = None) -> bool:
        if obj:
            default_permission = super().has_delete_permission(request, obj)
            if hasattr(obj, 'has_object_permission'):
                return default_permission or obj.has_object_permission(request)
            return default_permission
        return True

    def has_module_permission(self, request: HttpRequest) -> bool:
        return True


class CustomModelAdmin(CustomAdminPermissions, ModelAdmin):
    pass


class CustomTabularInline(CustomAdminPermissions, TabularInline):
    pass


class CustomStackedInline(CustomAdminPermissions, StackedInline):
    pass


class UserAdminAuthenticationForm(AuthenticationForm):
    required_css_class = 'required'


class UserAdminSite(AdminSite):

    site_title = gettext_lazy('Within budget')
    site_header = gettext_lazy('Within budget')
    index_title = gettext_lazy('My budget')

    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active


user_admin_site = UserAdminSite(name='usersadmin')
