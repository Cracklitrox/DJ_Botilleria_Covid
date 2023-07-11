from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('autentificacion_administrador/',views.autentificacion_administrador,name="autentificacion"),
    path('cerrar_sesion_admin/',views.cerrar_sesion_admin,name='cerrar_sesion_admin'),
    path('html/base_admin/',views.base_admin,name='base_admin'),
    path('productos/crear_productos/',views.crear_producto, name='crear_productos'),
    path('productos/admin_productos/',views.admin_productos, name='admin_productos'),
    path('productos/admin_opc_productos/',views.opc_productos,name='opciones_productos'),
    path('productos/encontrar_producto/<str:pk>',views.encontrar_producto, name='encontrar_producto'),
    path('productos/modificar_producto/',views.modificar_producto,name='modificar_producto'),
    path('productos/eliminar_producto/<str:pk>',views.eliminar_producto,name='eliminar_producto'),
    path('admindjango/crear_admin/',views.crear_admin, name='crear_admin'),
    path('admindjango/total_administradores/',views.total_administradores, name='total_administradores'),
    path('admindjango/admin_opc_admin/',views.admin_opc_admin,name='admin_opc_admin'),
    path('admindjango/encontrar_admin/<str:pk>',views.encontrar_admin, name='encontrar_admin'),
    path('admindjango/modificar_admin/',views.modificar_admin,name='modificar_admin'),
    path('admindjango/eliminar_admin/<str:pk>',views.eliminar_admin,name='eliminar_admin'),
    path('Imagen/subir_imagen/', views.subir_imagen, name='subir_imagen'),
    path('Imagen/admin_imagen/', views.admin_imagen, name='admin_imagen'),
    path('Imagen/opciones_imagen/', views.opciones_imagen, name='opciones_imagen'),
    path('Imagen/encontrar_imagen/<str:pk>', views.encontrar_imagen, name='encontrar_imagen'),
    path('Imagen/modificar_imagen/', views.modificar_imagen, name='modificar_imagen'),
    path('Imagen/eliminar_imagen/<str:pk>', views.eliminar_imagen, name='eliminar_imagen'),
    path('usuarios/crear_usuario/',views.crear_usuario, name='crear_usuario'),
    path('usuarios/admin_usuarios/',views.admin_usuario, name='admin_usuarios'),
    path('usuarios/opciones_usuario/',views.opciones_usuario,name='opciones_usuario'),
    path('usuarios/encontrar_usuario/<str:pk>',views.encontrar_usuario,name="encontrar_usuario"),
    path('usuarios/modificar_usuario/',views.modificar_usuario,name='modificar_usuario'),
    path('usuarios/eliminar_usuario/<str:pk>',views.eliminar_usuario,name='eliminar_usuario')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)