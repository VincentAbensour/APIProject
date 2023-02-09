from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.


class AccountAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'firstname', 'lastname']
    fieldsets = (
        (None,{'fields':('email', 'password')}),
        (
            'Identity', {'fields':
                                    ('firstname',
                                    'lastname',)}
        ),
        (
            'Permissions', {'fields':
                                    ('is_active',
                                    'is_staff',
                                    'is_admin',
                                    'is_superuser')}
        ),
        (
            'Dates', {'fields':('last_login',)}
        )
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
        'fields':(
            'email',
            'firstname',
            'lastname',
            'password1',
            'password2',
            'is_active',
            'is_staff',
            'is_admin',
            'is_superuser'
        )
        }),
    )



admin.site.register(Account, AccountAdmin)