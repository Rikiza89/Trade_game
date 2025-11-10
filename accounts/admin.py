from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'balance', 'total_value', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Game Data', {'fields': ('balance', 'total_value')}),
    )