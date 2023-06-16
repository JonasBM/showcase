from typing import Dict

from core.helpers.admin import CustomAdminPermissions, CustomModelAdmin, user_admin_site
from django.contrib import admin
from django.contrib.admin import register
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _

from budgets.models import Entry, Tag, Wallet


class EntryInline(CustomAdminPermissions, admin.TabularInline):
    model = Entry


@register(Wallet, site=user_admin_site)
class WalletAdmin(CustomModelAdmin):
    model = Wallet

    readonly_fields = ['balance']
    list_display = ['name', 'balance']
    ordering = ['user', 'name']
    search_fields = ['name']
    autocomplete_fields = ['user']
    inlines = [EntryInline, ]

    def get_list_display(self, request):
        if request.user.is_staff:
            return ['user', ] + self.list_display
        return self.list_display

    def get_queryset(self, request: HttpRequest) -> QuerySet[Wallet]:
        queryset = super().get_queryset(request)
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        return queryset

    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, str]:
        initial_data = super().get_changeform_initial_data(request)
        if not request.user.is_staff:
            initial_data['user'] = request.user
        return initial_data

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if not request.user.is_staff:
            if db_field.attname == 'user_id':
                queryset = queryset.filter(pk=request.user.pk)
        return queryset


@register(Tag, site=user_admin_site)
class TagAdmin(CustomModelAdmin):
    model = Tag

    list_display = ['name', 'type']
    ordering = ['user', 'name']
    search_fields = ['name', 'type']
    autocomplete_fields = ['user']
    list_filter = ['type']

    def get_list_display(self, request):
        if request.user.is_staff:
            return ['user', ] + self.list_display
        return self.list_display

    def get_queryset(self, request: HttpRequest) -> QuerySet[Wallet]:
        queryset = super().get_queryset(request)
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        return queryset

    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, str]:
        initial_data = super().get_changeform_initial_data(request)
        if not request.user.is_staff:
            initial_data['user'] = request.user
        return initial_data

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if not request.user.is_staff:
            if db_field.attname == 'user_id':
                queryset = queryset.filter(pk=request.user.pk)
        return queryset


class TagTypeListFilter(admin.SimpleListFilter):
    title = _('tag type')

    parameter_name = 'tag_type'

    def lookups(self, request, model_admin):
        return Tag.TYPE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__type=self.value()).distinct()
        return queryset


class TagNameListFilter(admin.SimpleListFilter):
    title = _('tag name')

    parameter_name = 'tag_name'

    def lookups(self, request, model_admin):
        queryset = Tag.objects
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        names = sorted(set(queryset.values_list('name', flat=True)))
        return [(name, name) for name in names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__name=self.value()).distinct()
        return queryset


@register(Entry, site=user_admin_site)
class EntryAdmin(CustomModelAdmin):
    model = Entry

    list_display = ['wallet', 'updated', 'tags_display', 'value']
    ordering = ['wallet__user', 'wallet__name', 'updated', 'id']
    search_fields = ['wallet', 'updated', 'value']
    autocomplete_fields = ['wallet']
    list_filter = ['wallet', TagTypeListFilter, TagNameListFilter]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Wallet]:
        queryset = super().get_queryset(request)
        if not request.user.is_staff:
            queryset = queryset.filter(wallet__user=request.user)
        return queryset

    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, str]:
        initial_data = super().get_changeform_initial_data(request)
        if not request.user.is_staff:
            initial_data['wallet'] = Wallet.objects.filter(user=request.user).first()
        return initial_data

    def get_field_queryset(self, db, db_field, request):
        queryset = super().get_field_queryset(db, db_field, request)
        if not request.user.is_staff:
            if db_field.attname == 'tags':
                queryset = queryset.filter(user=request.user)
            if db_field.attname == 'wallet_id':
                queryset = queryset.filter(user=request.user)
        return queryset
