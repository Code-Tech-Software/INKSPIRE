from django.urls import path

from . import views
from .views import *

app_name = 'productos'
urlpatterns = [
    path('crear/', crear_producto, name='crear_producto'),
    path('', producto_list, name='producto_list'),
    path('categoria/<uuid:id_categoria>/', producto_list, name='productos_por_categoria'),
    path('product-details/<uuid:id_producto>/', views.productDetails, name='productDetails'),
    path('cart', views.cart, name='cart'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_carrito'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),


    path('carrito/actualizar/', views.actualizar_item_carrito, name='actualizar_item_carrito'),
    path('carrito/eliminar/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('cart-data/', views.cart_data, name='cart_data'),
]
