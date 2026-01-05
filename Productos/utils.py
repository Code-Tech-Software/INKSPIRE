from .models import Carrito


def obtener_carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(
            usuario=request.user
        )
        return carrito

    if not request.session.session_key:
        request.session.create()

    carrito, _ = Carrito.objects.get_or_create(
        session_key=request.session.session_key
    )
    return carrito