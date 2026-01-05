from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from django.utils.translation import gettext_lazy as _

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    # campos añadidos en el modelo
    fieldsets = UserAdmin.fieldsets + (
        (_('Información adicional'), {'fields': ('telefono', 'url_imagen', 'rol')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Información adicional'), {'fields': ('telefono', 'url_imagen', 'rol')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
