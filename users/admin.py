from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.

class UserAdmin(BaseAdmin):
  ordering = ['id']
  list_display = ['email', 'name']
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    (
      _('Permissions'),
      {
        'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
        )
      }
    ),
    (
      _('Important dates'),
      {
        'fields': (
          'last_login',
        )
      }
    )
  )
  readonly_fields = ['last_login']
  add_fieldsets = (
    (None, {
      'classes': ('extrapretty',),
      'fields': (
        'email',
        'password1',
        'password2',
        'is_active',
        'is_staff',
        'is_superuser',
      )
    }),
  )

admin.site.register(User, UserAdmin)