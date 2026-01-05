import uuid
import json
from django.db import models
from django.core.exceptions import ValidationError

from django.db.models import JSONField



class Categoria(models.Model):
    id_categoria = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    visible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    class TipoProducto(models.TextChoices):
        FISICO = 'fisico', 'Físico'
        SERVICIO = 'servicio', 'Servicio'
        PERSONALIZADO = 'personalizado', 'Personalizado'

    id_producto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    descripcion_corta = models.CharField(max_length=512, blank=True)
    tipo_producto = models.CharField(max_length=20, choices=TipoProducto.choices, default=TipoProducto.FISICO)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sku = models.CharField(max_length=100, unique=True)
    maneja_stock = models.BooleanField(default=True)
    requiere_produccion = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    visible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class ImagenProducto(models.Model):
    id_imagen = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')
    es_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class OptionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='option_types')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.producto.nombre})"


class OptionValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    option_type = models.ForeignKey(OptionType, on_delete=models.CASCADE, related_name='values')
    valor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.valor} — {self.option_type.nombre}"

class ProductVariant(models.Model):
    id_variant = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variants')
    opciones = JSONField()
    sku = models.CharField(max_length=150, blank=True, null=True, unique=True)
    precio_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'sku')

    def __str__(self):
        if isinstance(self.opciones, dict):
            vals = " / ".join(str(v) for v in self.opciones.values())
        else:
            vals = str(self.opciones)
        return f"{self.producto.nombre} — {vals}"

    def clean(self):
        if not isinstance(self.opciones, dict):
            raise ValidationError("Las opciones deben guardarse como JSON/dict.")







class Carrito(models.Model):
    id_carrito = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'Usuarios.Usuario',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carritos'
    )
    session_key = models.CharField(max_length=40, db_index=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito {self.id_carrito}"


class CarritoItem(models.Model):
    id_item = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'producto', 'variante')

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"