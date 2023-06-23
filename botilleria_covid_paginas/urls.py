from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cerveza/', views.cerveza, name='cerveza'),
    path('contacto/', views.contacto, name='contacto'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('productos/', views.productos, name='productos'),
    path('reestablecer_contraseña/', views.reestablecer_contraseña, name='reestablecer_contraseña'),
    path('registro/', views.registro, name='registro'),
    path('vinos/', views.vinos, name='vinos'),
    path('whiskys/', views.whiskys, name='whiskys'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]