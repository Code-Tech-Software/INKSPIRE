import json
from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import Producto, ImagenProducto, OptionType, OptionValue, ProductVariant
from .utils import obtener_carrito


def crear_producto(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        imagenes = request.FILES.getlist('imagenes')

        # Recepción de JSON con info de variantes (en el template JS generamos y guardamos en un hidden)
        variants_info_json = request.POST.get('variants_info')  # tipos y valores
        variant_combinations_json = request.POST.get('variant_combinations')  # combinaciones con sku/stock/precio_extra

        if producto_form.is_valid() and len(imagenes) >= 1:
            producto = producto_form.save()

            # guardamos imágenes (marcando la primera como principal)
            for index, img in enumerate(imagenes):
                ImagenProducto.objects.create(
                    producto=producto,
                    imagen=img,
                    es_principal=(index == 0)
                )

            # guardar OptionType / OptionValue (si vienen)
            if variants_info_json:
                try:
                    variants_info = json.loads(variants_info_json)
                except Exception:
                    variants_info = []
                # variants_info expected: [{ "name": "Talla", "values": ["S","M","L"] }, ...]
                for ot in variants_info:
                    nombre = ot.get('name')
                    valores = ot.get('values', [])
                    if not nombre:
                        continue
                    option_type = OptionType.objects.create(producto=producto, nombre=nombre)
                    for v in valores:
                        OptionValue.objects.create(option_type=option_type, valor=v)

            # guardar las combinaciones (variantes)
            if variant_combinations_json:
                try:
                    variant_combinations = json.loads(variant_combinations_json)
                except Exception:
                    variant_combinations = []
                for comb in variant_combinations:
                    opciones = comb.get('opciones') or {}  # dict {"Talla":"M","Color":"Azul"}
                    sku = comb.get('sku') or None
                    precio_extra = comb.get('precio_extra') or 0
                    stock = comb.get('stock') or 0

                    # Si no viene sku, generamos uno por defecto: PRODUCTSKU-1, -2...
                    if not sku:
                        base = (producto.sku or producto.nombre[:6].upper()).replace(" ", "")
                        # contador simple
                        contador = ProductVariant.objects.filter(producto=producto).count() + 1
                        sku = f"{base}-{contador}"

                    # guardamos variante
                    ProductVariant.objects.create(
                        producto=producto,
                        opciones=opciones,
                        sku=sku,
                        precio_extra=precio_extra,
                        stock=stock
                    )

            # redirigir a la misma página (o a detalle)
            return redirect('productos:crear_producto')

        else:
            return render(request, 'productos/crear_producto.html', {
                'producto_form': producto_form,
                'form_errors': producto_form.errors,
            })

    else:
        producto_form = ProductoForm()

    return render(request, 'productos/crear_producto.html', {
        'producto_form': producto_form,
    })


from django.shortcuts import render, get_object_or_404
from .models import Producto


def producto_list(request):
    productos = Producto.objects.filter(visible=True).select_related('categoria')
    return render(request, 'productos/producto_list.html', {
        'productos': productos
    })


from django.core.serializers.json import DjangoJSONEncoder


def producto_detail(request, id_producto):
    producto = get_object_or_404(
        Producto.objects.prefetch_related(
            'imagenes',
            'variants',
            'option_types__values'
        ),
        id_producto=id_producto,
        visible=True
    )

    variantes = []
    for v in producto.variants.filter(activo=True):
        variantes.append({
            "id": str(v.id_variant),
            "opciones": v.opciones,
            "precio_extra": float(v.precio_extra),
            "stock": v.stock,
            "sku": v.sku,
        })

    return render(request, "productos/producto_detail.html", {
        "producto": producto,
        "variantes_json": json.dumps(variantes, cls=DjangoJSONEncoder),
    })


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Producto, ProductVariant, Carrito, CarritoItem


@require_POST
def agregar_al_carrito(request):
    producto_id = request.POST.get('producto_id')
    variante_id = request.POST.get('variante_id')
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad < 1:
        return JsonResponse({'error': 'Cantidad inválida'}, status=400)

    producto = Producto.objects.get(id_producto=producto_id)

    variante = None
    if variante_id:
        variante = ProductVariant.objects.get(
            id_variant=variante_id,
            producto=producto,
            activo=True
        )
        if variante.stock < cantidad:
            return JsonResponse({'error': 'Stock insuficiente'}, status=400)

    carrito = obtener_carrito(request)

    item, creado = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        variante=variante,
        defaults={'cantidad': cantidad}
    )

    if not creado:
        nueva_cantidad = item.cantidad + cantidad
        if variante and nueva_cantidad > variante.stock:
            return JsonResponse({'error': 'Stock insuficiente'}, status=400)

        item.cantidad = nueva_cantidad
        item.save()

    return JsonResponse({
        'success': True,
        'item_id': str(item.id_item),
        'cantidad': item.cantidad
    })


from django.shortcuts import render
from .models import Carrito

from .utils import obtener_carrito


def ver_carrito(request):
    carrito = obtener_carrito(request)

    items = []
    total = 0

    for item in carrito.items.select_related('producto', 'variante'):
        precio_unitario = item.producto.precio_base
        if item.variante:
            precio_unitario += item.variante.precio_extra

        subtotal = precio_unitario * item.cantidad
        total += subtotal

        items.append({
            'item': item,
            'precio_unitario': precio_unitario,
            'subtotal': subtotal
        })

    return render(request, 'productos/carrito.html', {
        'items': items,
        'total': total
    })


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Carrito, CarritoItem


@require_POST
def actualizar_item_carrito(request):
    item_id = request.POST.get('item_id')
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad < 1:
        return JsonResponse({'error': 'Cantidad inválida'}, status=400)

    carrito = obtener_carrito(request)

    item = carrito.items.select_related(
        'producto', 'variante'
    ).filter(
        id_item=item_id
    ).first()

    if not item:
        return JsonResponse({'error': 'Item no encontrado'}, status=404)

    if item.variante and cantidad > item.variante.stock:
        return JsonResponse({'error': 'Stock insuficiente'}, status=400)

    item.cantidad = cantidad
    item.save()

    precio_unitario = item.producto.precio_base
    if item.variante:
        precio_unitario += item.variante.precio_extra

    subtotal = precio_unitario * item.cantidad

    total = 0
    for i in carrito.items.all():
        pu = i.producto.precio_base
        if i.variante:
            pu += i.variante.precio_extra
        total += pu * i.cantidad

    return JsonResponse({
        'success': True,
        'subtotal': float(subtotal),
        'total': float(total),
        'cantidad': item.cantidad
    })


@require_POST
def eliminar_item_carrito(request):
    item_id = request.POST.get('item_id')

    carrito = obtener_carrito(request)

    item = carrito.items.filter(id_item=item_id).first()

    if not item:
        return JsonResponse({'error': 'Item no encontrado'}, status=404)

    item.delete()

    total = 0
    for i in carrito.items.all():
        pu = i.producto.precio_base
        if i.variante:
            pu += i.variante.precio_extra
        total += pu * i.cantidad

    return JsonResponse({
        'success': True,
        'total': float(total)
    })
