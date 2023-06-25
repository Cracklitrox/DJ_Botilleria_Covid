from django.shortcuts import render,get_object_or_404
from .models import Productos, Imagen, Admin_django, Almacen
import os
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.

def base_admin(request):
    return render(request, "base_admin.html")

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
        titulo = request.POST["titulo_producto"].strip()
        descripcion = request.POST["descripcion_producto"].strip()
        precio = request.POST["precio_producto"].strip()
        cantidad = request.POST["cantidad_producto"].strip()
        imagen = request.FILES.get("imagen")
        adicional = request.POST["informacion_adicional"].strip()
        if not (titulo and descripcion and precio and cantidad):
            context = {'mensaje': '❌ Error: Debe rellenar todos los campos obligatorios'}
            return render(request, 'html/productos/crear_productos.html', context)
        if not imagen:
            context = {'mensaje': '❌ Error: Debes seleccionar una imagen'}
            return render(request, 'html/productos/crear_productos.html', context)
        try:
            precio_int = int(precio)
            if precio_int <= 0:
                raise ValueError
        except ValueError:
            context = {'mensaje': '❌ Error: El precio debe ser un número entero positivo'}
            return render(request, 'html/productos/crear_productos.html', context)
        try:
            cantidad_int = int(cantidad)
            if cantidad_int <= 0:
                raise ValueError
        except ValueError:
            context = {'mensaje': '❌ Error: La cantidad debe ser un número entero positivo'}
            return render(request, 'html/productos/crear_productos.html', context)
        MAX_TITULO_LENGTH = 30
        MAX_DESCRIPCION_LENGTH = 50
        if len(titulo) > MAX_TITULO_LENGTH or len(descripcion) > MAX_DESCRIPCION_LENGTH:
            context = {'mensaje': f'❌ Error: El título y la descripción deben tener como máximo {MAX_TITULO_LENGTH} y {MAX_DESCRIPCION_LENGTH} caracteres respectivamente'}
            return render(request, 'html/productos/crear_productos.html', context)
        producto_campos = {
            "titulo_producto": titulo,
            "descripcion_producto": descripcion,
            "precio_producto": precio,
            "cantidad": cantidad,
            "imagen": imagen,
            "informacion_adicional": adicional
        }
        producto = Productos.objects.create(**producto_campos)
        context = {'mensaje': '✔ Producto guardado con éxito', 'producto': producto}
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
        titulo = request.POST["titulo"].strip()
        descripcion = request.POST["descripcion"]
        precio = request.POST["precio"].strip()
        cantidad = request.POST["cantidad_producto"].strip()
        imagen = request.FILES.get("imagen")
        adicional = request.POST.get("adicional", "")
        cambios_realizados = False
        mensaje = ""
        if titulo and productos.titulo_producto != titulo:
            productos.titulo_producto = titulo
            cambios_realizados = True
        if descripcion and productos.descripcion_producto != descripcion:
            productos.descripcion_producto = descripcion
            cambios_realizados = True
        if precio:
            try:
                precio_int = int(precio)
                if precio_int <= 0:
                    raise ValueError
                if productos.precio_producto != precio_int:
                    productos.precio_producto = precio_int
                    cambios_realizados = True
            except ValueError:
                mensaje = "❌ Error: El precio debe ser un número entero positivo"
        if cantidad:
            try:
                cantidad_int = int(cantidad)
                if cantidad_int <= 0:
                    raise ValueError
                if productos.cantidad != cantidad_int:
                    productos.cantidad = cantidad_int
                    cambios_realizados = True
            except ValueError:
                mensaje = "❌ Error: La cantidad debe ser un número entero positivo"
        if imagen:
            if productos.imagen:
                ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, str(productos.imagen))
                if os.path.isfile(ruta_imagen_anterior):
                    os.remove(ruta_imagen_anterior)
            productos.imagen = imagen
            cambios_realizados = True
        if imagen:
            productos.imagen = imagen
            cambios_realizados = True
        if productos.informacion_adicional != adicional:
            productos.informacion_adicional = adicional
            cambios_realizados = True
        if cambios_realizados:
            productos.save()
            mensaje = "✔ Producto actualizado con éxito"
        elif not mensaje:
            mensaje = "No se realizaron cambios en el producto"
        context = {"mensaje": mensaje, "productos": productos}
        return render(request, "html/productos/modificar_producto.html", context)
    else:
        productos = Productos.objects.all()
        context = {"productos": productos}
        return render(request, "html/productos/admin_opc_productos.html", context)

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
        nombre_admin = request.POST["nombre_admin"].strip()
        contrasena_admin = request.POST["contrasena_admin"].strip()
        confirmar_contrasena_admin = request.POST["confirmar_contrasena_admin"].strip()
        if nombre_admin == "" or contrasena_admin == "" or confirmar_contrasena_admin == "":
            context = {'mensaje': '❌ Error: Todos los campos son obligatorios'}
        elif contrasena_admin == confirmar_contrasena_admin:
            if User.objects.filter(username=nombre_admin).exists():
                context = {'mensaje': '❌ Error: El nombre de administrador ya está en uso'}
            else:
                User.objects.create_superuser(username=nombre_admin, password=contrasena_admin)
                campos_admin = {
                    "nombre_admin": nombre_admin,
                    "contrasena_admin": contrasena_admin
                }
                admin_django = Admin_django.objects.create(**campos_admin)
                context = {'mensaje': '✔ Administrador creado con éxito', 'admin_django': admin_django}
        else:
            context = {'mensaje': '❌ Error: Las contraseñas deben ser iguales'}
        return render(request, 'html/admindjango/crear_admin.html', context)
    else:
        return render(request, 'html/admindjango/crear_admin.html')

def encontrar_admin(request, pk):
    if pk != " ":
        admin_dj = Admin_django.objects.get(id_admin=pk)
        context={'admin_dj':admin_dj}
    if admin_dj:
        return render(request,'html/admindjango/modificar_admin.html',context)
    else:
        context={'mensaje':'❌ Error, id de la imagen no encontrada'}
        return render(request,'html/admindjango/admin_opc_admin.html',context)

def modificar_admin(request):
    if request.method == "POST":
        id_admin = request.POST["id_admin"]
        admin_dj = get_object_or_404(Admin_django, id_admin=id_admin)
        nombre_admin = request.POST["nombre_admin"].strip()
        contrasena_admin = request.POST["contrasena_admin"]
        contrasena_nueva1 = request.POST["contrasena_nueva1"].strip()
        contrasena_nueva2 = request.POST["contrasena_nueva2"].strip()
        cambios_realizados = False
        mensaje = ''
        if nombre_admin != "":
            if nombre_admin != admin_dj.nombre_admin.strip():
                if Admin_django.objects.filter(nombre_admin=nombre_admin).exists():
                    mensaje = '❌ Error: El nombre de administrador ya está en uso'
                else:
                    admin_dj.nombre_admin = nombre_admin
                    cambios_realizados = True
        if contrasena_nueva1 != "" or contrasena_nueva2 != "":
            if contrasena_nueva1 != contrasena_admin:
                if contrasena_nueva1 == contrasena_nueva2:
                    admin_dj.contrasena_admin = contrasena_nueva1
                    cambios_realizados = True
                else:
                    mensaje = '❌ Error: Las contraseñas nuevas deben ser iguales'
            else:
                mensaje = '❌ Error: La contraseña nueva no puede ser igual a la anterior'
        elif not cambios_realizados:
            mensaje = '❌ Error: No se ha realizado ningún cambio'
        if cambios_realizados:
            admin_dj.save()
            mensaje = '✔ Administrador actualizado con éxito'
        context = {'mensaje': mensaje, 'admin_dj': admin_dj}
        return render(request, 'html/admindjango/modificar_admin.html', context)
    else:
        admin_dj = Admin_django.objects.all()
        context = {'admin_dj': admin_dj}
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
def opciones_imagen(request):
    imagen = Imagen.objects.all()
    context = {'imagen':imagen}
    return render(request, 'html/Imagen/opciones_imagen.html', context)

def admin_imagen(request):
    imagen = Imagen.objects.all()
    context = {'imagen':imagen}
    return render(request, 'html/Imagen/admin_imagen.html', context)

def subir_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get("imagen")
        descripcion_imagen = request.POST["descripcion_imagen"]
        if imagen and not descripcion_imagen.isspace():
            productos_campos = {
                "imagen": imagen,
                "descripcion_imagen": descripcion_imagen
            }
            imagen = Imagen.objects.create(**productos_campos)
            context = {'mensaje': '✔ Imagen guardada con éxito', 'imagen': imagen}
            return render(request, 'html/Imagen/subir_imagen.html', context)
        else:
            context = {'mensaje': '❌ Error: Debes completar todos los campos obligatorios'}
            return render(request, 'html/Imagen/subir_imagen.html', context)
    else:
        return render(request, 'html/Imagen/subir_imagen.html')



def encontrar_imagen(request,pk):
    if pk != " ":
        imagen = Imagen.objects.get(id_imagen=pk)
        context={'imagen':imagen}
    if imagen:
        return render(request,'html/Imagen/modificar_imagen.html',context)
    else:
        context={'mensaje':'❌ Error, id de la imagen no encontrada'}
        return render(request,'html/Imagen/opciones_imagen.html',context)

def modificar_imagen(request):
    if request.method == "POST":
        id_imagen = request.POST["id_imagen"]
        imagen = get_object_or_404(Imagen, id_imagen=id_imagen)
        file_imagen = request.FILES.get("file_imagen")
        descripcion_imagen = request.POST["descripcion_imagen"]
        cambios_realizados = False
        if file_imagen:
            if imagen.imagen:
                ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
                if os.path.isfile(ruta_imagen_anterior):
                    os.remove(ruta_imagen_anterior)
            imagen.imagen = file_imagen
            cambios_realizados = True
        if imagen.descripcion_imagen != descripcion_imagen:
            imagen.descripcion_imagen = descripcion_imagen
            cambios_realizados = True
        if cambios_realizados:
            imagen.save()
            mensaje = '✔ Imagen actualizada con éxito'
        else:
            mensaje = 'No se realizaron cambios en la imagen'
        context = {'mensaje': mensaje, 'imagen': imagen}
        return render(request, 'html/Imagen/modificar_imagen.html', context)
    else:
        imagen = Imagen.objects.all()
        context = {'imagen': imagen}
        return render(request, 'html/Imagen/opciones_imagen.html', context)

def eliminar_imagen(request, pk):
    context = {}
    try:
        imagenes = Imagen.objects.get(id_imagen=pk)
        imagen_url = imagenes.imagen.url
        imagenes.delete()
        if imagen_url:
            ruta_imagen = os.path.abspath(os.path.join(settings.MEDIA_ROOT, imagen_url.replace('/media/', '')))
            if os.path.isfile(ruta_imagen):
                os.remove(ruta_imagen)
                context = {'mensaje': '☠ Imagen eliminada con exito'}
        imagenes = Imagen.objects.all()
        context['imagenes'] = imagenes
        return render(request, 'html/Imagen/opciones_imagen.html', context)
    except Imagen.DoesNotExist:
        imagenes = Imagen.objects.all()
        context = {'imagenes': imagenes, 'mensaje': '🤷 Error, id de la imagen no encontrada'}
        return render(request, 'html/Imagen/opciones_imagen.html', context)