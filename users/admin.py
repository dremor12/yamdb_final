from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'role', 'bio'
    )
    fields = (
        'username', 'email', 'role', 'bio'
    )
    search_fields = ('username', 'email', 'role')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
