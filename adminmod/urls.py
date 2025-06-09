from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin, name='adminlogin'),
    path('panel_admin/', views.panel_admin, name='panel_admin'), 
    path('admin_productos/', views.admin_productos, name='admin_productos'),
    path('admin_productos/crear/', views.admin_producto_crear, name='admin_producto_crear'),
    path('admin_productos/editar/<int:producto_id>/', views.admin_producto_editar, name='admin_producto_editar'),
    path('admin_productos/eliminar/<int:producto_id>/', views.admin_producto_eliminar, name='admin_producto_eliminar'),
    path('admin_usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('users_basicos/', views.users_basicos, name='users_basicos'),
    path('eliminar_user/<int:usuario_id>/', views.eliminar_user, name='eliminar_user'),
    path('users_admins/', views.users_admins, name='users_admins'),
    path('modificar_user_admin/<int:usuario_id>/', views.modificar_user_admin, name='modificar_user_admin'),
    path('eliminar_user_admin/<int:usuario_id>/', views.eliminar_user_admin, name='eliminar_user_admin'),
    path('register_user_admin/', views.register_user_admin, name='register_user_admin'),
    path('modificar_user_admin/<int:usuario_id>/', views.modificar_user_admin, name='modificar_user_admin'),
    path('admin_ventas/', views.admin_ventas, name='admin_ventas'),  
    path('admin_logout/', views.admin_logout_view, name='admin_logout'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
]