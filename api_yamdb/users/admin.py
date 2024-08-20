from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import YaUser


class YaAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
    list_filter = ('is_active', 'role',)
    list_editable = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('bio', 'role')}),
    )


admin.site.register(YaUser, YaAdmin)
