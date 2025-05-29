
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
    path('formulario_registro/', views.formulario_registro, name='formulario_registro'),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('carrito/agregar/ajax/', views.agregar_carrito_ajax, name='agregar_carrito_ajax'),
    path('api/carrito/<int:carrito_id>/', views.api_carrito, name='api_carrito'),

]
