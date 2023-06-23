from django.shortcuts import render,get_object_or_404
from .models import Productos, Imagen, Admin_django
import os
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.

# Funciones Productos
def opc_productos(request):
    productos = Productos.objects.all()
    context = {'productos':productos}
    return render(request, 'html/productos/admin_opc_productos.html', context)

def admin_productos(request):
    productos = Productos.objects.all()
    context = {'productos':productos}
    return render(request, 'html/productos/admin_productos.html', context)

def crear_producto(request):
    if request.method == "POST":
        titulo = request.POST["titulo_producto"]
        descripcion = request.POST["descripcion_producto"]
        precio = request.POST["precio_producto"]
        imagen = request.FILES.get("imagen")
        adicional = request.POST["informacion_adicional"]
        
        if titulo and descripcion and precio and imagen:
            productos_campos = {
                "titulo_producto" : titulo,
                "descripcion_producto" : descripcion,
                "precio_producto" : precio,
                "imagen" : imagen,
                "informacion_adicional" : adicional
            }
            productos = Productos.objects.create(**productos_campos)
            context = {'mensaje': '✔ Producto guardado con éxito', 'productos': productos}
            return render(request, 'html/productos/crear_productos.html', context)
        else:
            context = {'mensaje': '❌ Error: Debes completar todos los campos obligatorios'}
            return render(request, 'html/productos/crear_productos.html', context)
    else:
        return render(request, 'html/productos/crear_productos.html')

def encontrar_producto(request,pk):
    if pk != " ":
        productos = Productos.objects.get(id_producto=pk)
    context={'productos':productos}
    if productos:
        return render(request,'html/productos/modificar_producto.html',context)
    else:
        context={'mensaje':'❌ Error, id producto no encontrado'}
        return render(request,'html/productos/admin_opc_productos.html',context)

def modificar_producto(request):
    if request.method == "POST":
        id_producto = request.POST["id_producto"]
        productos = get_object_or_404(Productos, id_producto=id_producto)
        titulo = request.POST["titulo"]
        descripcion = request.POST["descripcion"]
        precio = request.POST["precio"]
        imagen = request.FILES.get("imagen")
        adicional = request.POST["adicional"]
        cambios_realizados = False
        if productos.titulo_producto != titulo:
            productos.titulo_producto = titulo
            cambios_realizados = True
        if productos.descripcion_producto != descripcion:
            productos.descripcion_producto = descripcion
            cambios_realizados = True
        if productos.precio_producto != precio:
            productos.precio_producto = precio
            cambios_realizados = True
        if imagen:
            productos.imagen = imagen
            cambios_realizados = True
        if productos.informacion_adicional != adicional:
            productos.informacion_adicional = adicional
            cambios_realizados = True
        if cambios_realizados:
            productos.save()
            mensaje = '✔ Producto actualizado con éxito'
        else:
            mensaje = 'No se realizaron cambios en el producto'
        context = {'mensaje': mensaje, 'productos': productos}
        return render(request, 'html/productos/modificar_producto.html', context)
    else:
        productos = Productos.objects.all()
        context = {'productos': productos}
        return render(request, 'html/productos/admin_opc_productos.html', context)

def eliminar_producto(request, pk):
    context = {}
    try:
        producto = Productos.objects.get(id_producto=pk)
        imagen_url = producto.imagen.url
        producto.delete()
        if imagen_url:
            ruta_imagen = os.path.abspath(os.path.join(settings.MEDIA_ROOT, imagen_url.replace('/media/', '')))
            if os.path.isfile(ruta_imagen):
                os.remove(ruta_imagen)
                context = {'mensaje': '☠ Producto eliminado correctamente'}
        productos = Productos.objects.all()
        context['productos'] = productos
        return render(request, 'html/productos/admin_opc_productos.html', context)
    except Productos.DoesNotExist:
        productos = Productos.objects.all()
        context = {'productos': productos, 'mensaje': '🤷 Error, id del producto no encontrado'}
        return render(request, 'html/productos/admin_opc_productos.html', context)

def listar_cervezas(request):
    productos = Productos.objects.all()
    return render(request, 'botilleria_covid_paginas/templates/html/cerveza.html',{'productos':productos})

# Funciones AdminDjango
def admin_opc_admin(request):
    admin_dj = Admin_django.objects.all()
    context = {'admin_dj':admin_dj}
    return render(request, 'html/admindjango/admin_opc_admin.html', context)

def total_administradores(request):
    admin_dj = Admin_django.objects.all()
    context = {'admin_dj':admin_dj}
    return render(request, 'html/admindjango/total_administradores.html', context)

def crear_admin(request):
    if request.method == "POST":
        nombre_admin = request.POST["nombre_admin"]
        contrasena_admin = request.POST["contrasena_admin"]
        confirmar_contrasena_admin = request.POST["confirmar_contrasena_admin"]
        if contrasena_admin == confirmar_contrasena_admin:
            User.objects.create_superuser(username=nombre_admin, password=contrasena_admin)
            campos_admin = {
                "nombre_admin" : nombre_admin,
                "contrasena_admin" : contrasena_admin
            }
            admin_django = Admin_django.objects.create(**campos_admin)
            context = {'mensaje': '✔ Producto guardado con éxito', 'admin_django': admin_django}
            return render(request, 'html/admindjango/crear_admin.html', context)
        else:
            context = {'mensaje': '❌ Error: Las contraseñas deben ser iguales'}
            return render(request, 'html/admindjango/crear_admin.html', context)
    else:
        return render(request, 'html/admindjango/crear_admin.html')

def encontrar_admin(request,pk):
    if pk != " ":
        admin_dj2 = Admin_django.objects.get(id_admin=pk)
    context={'admin_dj':admin_dj2}
    if admin_dj2:
        return render(request,'html/admindjango/admin_opc_admin.html',context)
    else:
        context={'mensaje':'❌ Error, id admin no encontrado'}
        return render(request,'html/admindjango/admin_opc_admin.html',context)

def modificar_admin(request):
    if request.method == "POST":
        id_admin = request.POST["id_admin"]
        admin_dj = get_object_or_404(Admin_django, id_admin=id_admin)
        nombre_admin = request.POST["nombre_admin"]
        contrasena_admin = request.POST["contrasena_admin"]
        cambios_realizados = False
        if admin_dj.nombre_admin != nombre_admin:
            admin_dj.nombre_admin = nombre_admin
            cambios_realizados = True
        if admin_dj.contrasena_admin != contrasena_admin:
            admin_dj.contrasena_admin = contrasena_admin
            cambios_realizados = True
        if cambios_realizados:
            admin_dj.save()
            mensaje = '✔ Administrador actualizado con éxito'
        else:
            mensaje = 'No se realizaron cambios en el administrador'
        context = {'mensaje': mensaje, 'adming_dj': adming_dj}
        return render(request, 'html/admindjango/modificar_admin.html', context)
    else:
        adming_dj = Admin_django.objects.all()
        context = {'adming_dj': adming_dj}
        return render(request, 'html/admindjango/admin_opc_admin.html', context)

def eliminar_admin(request, pk):
    context = {}
    try:
        admin_dj = Admin_django.objects.get(id_admin=pk)
        admin_dj.delete()
        admin_dj_total = Admin_django.objects.all()
        context['admin_dj_total'] = admin_dj_total
        return render(request, 'html/admindjango/admin_opc_admin.html', context)
    except Admin_django.DoesNotExist:
        admin_dj = Admin_django.objects.all()
        context = {'admin_dj': admin_dj, 'mensaje': '🤷 Error, id del administrador no encontrado'}
        return render(request, 'html/admindjango/admin_opc_admin.html', context)

# Funciones Imagen
def subir_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get("imagen")
        descripcion_imagen = request.POST["descripcion_imagen"]
        if imagen and descripcion_imagen:
            productos_campos = {
                "imagen" : imagen,
                "descripcion_imagen" : descripcion_imagen
            }
            imagen = Imagen.objects.create(**productos_campos)
            context = {'mensaje': '✔ Producto guardado con éxito', 'imagen': imagen}
            return render(request, 'html/Imagen/subir_imagen.html', context)
        else:
            context = {'mensaje': '❌ Error: Debes completar todos los campos obligatorios'}
            return render(request, 'html/Imagen/subir_imagen.html', context)
    else:
        return render(request, 'html/Imagen/subir_imagen.html')

# Funciones Almacen
# def opc_almacen(request):
#     # Obtiene todos los registros de Almacen
#     almacen = Almacen.objects.all()
#     context = {'almacen': almacen}
#     return render(request, 'html/almacen/admin_opc_almacen.html', context)

# def admin_almacen(request):
#     # Obtiene todos los registros de Almacen
#     almacen = Almacen.objects.all()
#     context = {'almacen': almacen}
#     return render(request, 'html/almacen/admin_almacen.html', context)

# def almacen_producto_cantidad(request):
#     if request.method == "POST":
#         id_producto = request.POST["id_producto"]
#         cantidad = request.POST["cantidad"]
#         if id_producto and cantidad:
#             campos_almacen = {
#                 "id_producto": id_producto,
#                 "cantidad": cantidad
#             }
#             # Crea un nuevo registro en Almacen con los campos proporcionados
#             almacen = Almacen.objects.create(**campos_almacen)
#             context = {'mensaje': '✔ Producto guardado con éxito', 'almacen': almacen}
#             return render(request, 'html/stock_almacen.html', context)
#         else:
#             context = {'mensaje': '❌ Error: Debes completar todos los campos obligatorios'}
#             return render(request, 'html/almacen/stock_almacen.html', context)
#     else:
#         return render(request, 'html/almacen/stock_almacen.html')

# def encontrar_id_almacen(request, pk):
#     if pk != " ":
#         almacen = Almacen.objects.get(id_producto=pk)
#     context = {'almacen': almacen}
#     if almacen:
#         return render(request, 'html/almacen/modificar_almacen.html', context)
#     else:
#         context = {'mensaje': 'Error, id producto no encontrado'}
#         return render(request, 'html/almacen/admin_opc_almacen.html', context)

# def modificar_cantidad_producto_almacen(request):
#     if request.method == "POST":
#         id_producto_id = request.POST["id_producto_id"]
#         almacen = get_object_or_404(Almacen, id_producto_id=id_producto_id)
#         cantidad = request.POST["cantidad"]
#         cambios_realizados = False
#         if almacen.cantidad != cantidad:
#             almacen.cantidad = cantidad
#             cambios_realizados = True
#         if cambios_realizados:
#             almacen.save()
#             mensaje = '✔ Producto actualizado con éxito'
#         else:
#             mensaje = 'No se realizaron cambios en el producto'
#         context = {'mensaje': mensaje, 'almacen': almacen}
#         return render(request, 'html/almacen/modificar_almacen.html', context)
#     else:
#         almacen = Almacen.objects.all()
#         context = {'almacen': almacen}
#         return render(request, 'html/almacen/modificar_almacen.html', context)

# def eliminar_cantidad_producto_almacen(request, pk):
#     context = {}
#     try:
#         almacen = Almacen.objects.get(id_producto_id=pk)
#         almacen.delete()
#         context = {'mensaje': '☠ Producto eliminado correctamente'}
#         almacen = Almacen.objects.all()
#         context['almacen'] = almacen
#         return render(request, 'html/almacen/admin_opc_almacen.html', context)
#     except Almacen.DoesNotExist:
#         almacen = Almacen.objects.all()
#         context = {'almacen': almacen, 'mensaje': '🤷 Error, id del producto no encontrado'}
#         return render(request, 'html/almacen/admin_opc_almacen.html', context)