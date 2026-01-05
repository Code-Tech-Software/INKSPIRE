from django.contrib import admin
from .models import Categoria, Producto, ImagenProducto

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]
    list_display = ('nombre', 'categoria', 'precio_base', 'visible')
    prepopulated_fields = {'sku': ('nombre',)}

admin.site.register(Categoria)
