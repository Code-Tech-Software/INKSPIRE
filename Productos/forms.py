from django import forms
from .models import Producto, ImagenProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'descripcion_corta',
            'tipo_producto',
            'precio_base',
            'costo',
            'sku',
            'maneja_stock',
            'requiere_produccion',
            'categoria',
            'visible',
        ]


class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['imagen', 'es_principal']




