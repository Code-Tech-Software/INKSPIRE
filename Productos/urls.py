from django.urls import path

from . import views
from .views import *

app_name = 'productos'
urlpatterns = [
    path('crear/', crear_producto, name='crear_producto'),
    path('', views.producto_list, name='lista'),
    path('<uuid:id_producto>/', views.producto_detail, name='detalle'),

    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_carrito'),

path('carrito/', views.ver_carrito, name='ver_carrito'),


path('carrito/actualizar/', views.actualizar_item_carrito, name='actualizar_item_carrito'),
path('carrito/eliminar/', views.eliminar_item_carrito, name='eliminar_item_carrito'),


]
