
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('carrito/<int:carrito_id>/', views.carrito, name='carrito'),
    path('carrito/<int:carrito_id>/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('agregar_carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('ventas/', views.ventas_resumen, name='ventas'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('carrito/<int:carrito_id>/eliminar/<int:producto_id>/', views.eliminar_producto_del_carrito, name='eliminar_producto_del_carrito'),
    path('carrito/<int:carrito_id>/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
]
