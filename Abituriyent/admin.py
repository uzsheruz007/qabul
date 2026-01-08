from django.contrib import admin
from .models import Privilege, PrivilegeCategory

from .models import QabulKvotasi
from django.shortcuts import render

@admin.register(PrivilegeCategory)
class PrivilegeCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "icon", "is_active")
    list_editable = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    ordering = ("order",)

@admin.register(QabulKvotasi)
class QabulKvotasiAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
