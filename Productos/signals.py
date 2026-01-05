from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import Carrito, CarritoItem


@receiver(user_logged_in)
def fusionar_carritos(sender, request, user, **kwargs):

    if not request.session.session_key:
        return

    carrito_sesion = Carrito.objects.filter(
        session_key=request.session.session_key
    ).first()

    if not carrito_sesion:
        return

    carrito_usuario, _ = Carrito.objects.get_or_create(
        usuario=user
    )

    for item in carrito_sesion.items.all():

        existente = CarritoItem.objects.filter(
            carrito=carrito_usuario,
            producto=item.producto,
            variante=item.variante
        ).first()

        if existente:
            existente.cantidad += item.cantidad
            existente.save()
            item.delete()
        else:
            item.carrito = carrito_usuario
            item.save()

    carrito_sesion.delete()
