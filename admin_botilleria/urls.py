from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('productos/crear_productos/',views.crear_producto, name='crear_productos'),
    path('productos/admin_productos/',views.admin_productos, name='admin_productos'),
    path('productos/admin_opc_productos/',views.opc_productos,name='opciones_productos'),
    path('productos/encontrar_producto/<str:pk>',views.encontrar_producto, name='encontrar_producto'),
    path('productos/modificar_producto/',views.modificar_producto,name='modificar_producto'),
    path('productos/eliminar_producto/<str:pk>',views.eliminar_producto,name='eliminar_producto'),
    path('admindjango/crear_admin/',views.crear_admin, name='crear_admin'),
    path('admindjango/total_administradores/',views.total_administradores, name='total_administradores'),
    path('admindjango/admin_opc_admin/',views.admin_opc_admin,name='admin_opc_admin'),
    path('admindjango/encontrar_admin/<int:pk>',views.encontrar_admin, name='encontrar_admin'),
    path('admindjango/modificar_admin/',views.modificar_admin,name='modificar_admin'),
    path('admindjango/eliminar_admin/<int:pk>',views.eliminar_admin,name='eliminar_admin'),
    path('Imagen/subir_imagen/', views.subir_imagen, name='subir_imagen'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)