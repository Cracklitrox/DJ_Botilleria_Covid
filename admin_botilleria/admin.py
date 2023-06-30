from django.contrib import admin
from .models import Admin_django, Productos, Carrito, Carrito_Productos, Compras, Compras_Productos, Imagen

# Register your models here.

admin.site.register(Admin_django)
admin.site.register(Productos)
admin.site.register(Carrito)
admin.site.register(Carrito_Productos)
admin.site.register(Compras)
admin.site.register(Compras_Productos)
admin.site.register(Imagen)