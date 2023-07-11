from django.shortcuts import render,get_object_or_404,redirect
from .models import Productos, Imagen, Admin_django
from botilleria_covid_paginas.models import Usuario,Contacto
import os
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.
# Funcion de autentificacion para el panel de administrador
def autentificacion_administrador(request):
    if request.method == 'POST':
        nombre_admin = request.POST['nombre_admin']
        contrasena_admin = request.POST['contrasena_admin']
        try:
            admin = Admin_django.objects.get(nombre_admin=nombre_admin, contrasena_admin=contrasena_admin)
            request.session['admin_id'] = admin.id_admin
            request.session['admin_nivel'] = admin.nivel_administrador
            return redirect('base_admin')
        except Admin_django.DoesNotExist:
            mensaje = 'Nombre de administrador o contraseña incorrectos. Por favor, inténtelo nuevamente.'
            return render(request, 'autentificacion_administrador.html', {'mensaje': mensaje})
    else:
        return render(request, 'autentificacion_administrador.html')

# Funcion para verificar que el administrador sea el que acceda al panel
def verificar_permisos(request):
    admin_nivel = request.session.get('admin_nivel')
    if admin_nivel is None:
        mensaje_logueo = 'Usted no tiene permisos para acceder al siguiente sitio, por favor inicie sesión.'
        return render(request, 'autentificacion_administrador.html', {'mensaje_logueo': mensaje_logueo})
    else:
        admin_id = request.session.get('admin_id')
        admin = Admin_django.objects.get(id_admin=admin_id)
        admin_nombre = admin.nombre_admin
        return admin_nombre

# Funcion para cerrar la sesion del administrador
def cerrar_sesion_admin(request):
    del request.session['admin_id']
    del request.session['admin_nivel']
    return redirect('autentificacion')

# Funcion para verificar el nivel de permisos que tiene el administrador
def verificar_permisos_admin(request,nivel_permiso,template_path,vista_funcion):
    admin_nombre = verificar_permisos(request)
    if admin_nombre is None:
        return redirect('autentificacion')
    else:
        admin_nivel = request.session.get('admin_nivel')
        if admin_nivel == nivel_permiso:
            return vista_funcion(request)
        else:
            admin_id = request.session.get('admin_id')
            admin = Admin_django.objects.get(id_admin=admin_id)
            admin_nombre = admin.nombre_admin
            mensaje_permisos = 'Lo siento, no tiene permisos para acceder al siguiente modelo, por favor consulte con su administrador principal.'
            return render(request,'html/base_admin.html',{'mensaje_permisos':mensaje_permisos,'admin_nombre':admin_nombre})

# Funcion Panel de administracion
def base_admin(request):
    admin_nombre = verificar_permisos(request)
    return render(request, 'html/base_admin.html', {'admin_nombre': admin_nombre})

# Funciones Productos
def opc_productos(request):
    def opc_productos_inner(request):
        productos = Productos.objects.all()
        context = {'productos':productos}
        return render(request, 'html/productos/admin_opc_productos.html', context)
    return verificar_permisos_admin(request,3,'html/productos/admin_opc_productos.html',opc_productos_inner)

def admin_productos(request):
    def admin_productos_inner(request):
        productos = Productos.objects.all()
        context = {'productos': productos}
        return render(request, 'html/productos/admin_productos.html', context)
    return verificar_permisos_admin(request,3,'html/productos/admin_productos.html',admin_productos_inner)

def crear_producto(request):
    def crear_producto_inner(request):
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
    return verificar_permisos_admin(request,3,'html/productos/crear_productos.html',crear_producto_inner)

def encontrar_producto(request,pk):
    def encontrar_producto_inner(request):
        if pk != " ":
            productos = Productos.objects.get(id_producto=pk)
            context={'productos':productos}
        if productos:
            return render(request,'html/productos/modificar_producto.html',context)
        else:
            context={'mensaje':'❌ Error: ID del producto no encontrado'}
            return render(request,'html/productos/admin_opc_productos.html',context)
    return verificar_permisos_admin(request,3,'html/productos/modificar_producto.html',encontrar_producto_inner)

def modificar_producto(request):
    def modificar_producto_inner(request):
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
    return verificar_permisos_admin(request,3,'html/productos/modificar_producto.html',modificar_producto_inner)

def eliminar_producto(request, pk):
    def eliminar_producto_inner(request):
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
            context = {'productos': productos, 'mensaje': '🤷 Error: ID del producto no encontrado'}
            return render(request, 'html/productos/admin_opc_productos.html', context)
    return verificar_permisos_admin(request,3,'html/productos/admin_opc_productos.html',eliminar_producto_inner)

# Funciones AdminDjango
def admin_opc_admin(request):
    def admin_opc_admin_inner(request):
        admin_dj = Admin_django.objects.all()
        context = {'admin_dj':admin_dj}
        return render(request, 'html/admindjango/admin_opc_admin.html', context)
    return verificar_permisos_admin(request,3,'html/admindjango/admin_opc_admin.html',admin_opc_admin_inner)

def total_administradores(request):
    def total_administradores_inner(request):
        admin_dj = Admin_django.objects.all()
        context = {'admin_dj':admin_dj}
        return render(request, 'html/admindjango/total_administradores.html', context)
    return verificar_permisos_admin(request,3,'html/admindjango/total_administradores.html',total_administradores_inner)

def crear_admin(request):
    def crear_admin_inner(request):
        if request.method == "POST":
            nombre_admin = request.POST["nombre_admin"].strip()
            contrasena_admin = request.POST["contrasena_admin"].strip()
            confirmar_contrasena_admin = request.POST["confirmar_contrasena_admin"].strip()
            nivel_administrador = request.POST["nivel_administrador"].strip()
            if nombre_admin == "" or contrasena_admin == "" or confirmar_contrasena_admin == "" or nivel_administrador == "":
                context = {'mensaje': '❌ Error: Todos los campos son obligatorios'}
            elif contrasena_admin == confirmar_contrasena_admin:
                if User.objects.filter(username=nombre_admin).exists():
                    context = {'mensaje': '❌ Error: El nombre de administrador ya está en uso'}
                else:
                    User.objects.create_superuser(username=nombre_admin, password=contrasena_admin)
                    campos_admin = {
                        "nombre_admin": nombre_admin,
                        "contrasena_admin": contrasena_admin,
                        "nivel_administrador" : nivel_administrador
                    }
                    admin_django = Admin_django.objects.create(**campos_admin)
                    context = {'mensaje': '✔ Administrador creado con éxito', 'admin_django': admin_django}
            else:
                context = {'mensaje': '❌ Error: Las contraseñas deben ser iguales'}
            return render(request, 'html/admindjango/crear_admin.html', context)
        else:
            return render(request, 'html/admindjango/crear_admin.html')
    return verificar_permisos_admin(request,3,'html/admindjango/crear_admin.html',crear_admin_inner)

def encontrar_admin(request, pk):
    def encontrar_admin_inner(request):
        if pk != " ":
            admin_dj = Admin_django.objects.get(id_admin=pk)
            context={'admin_dj':admin_dj}
        if admin_dj:
            return render(request,'html/admindjango/modificar_admin.html',context)
        else:
            context={'mensaje':'❌ Error, id del administrador no encontrado'}
            return render(request,'html/admindjango/admin_opc_admin.html',context)
    return verificar_permisos_admin(request,3,'html/admindjango/modificar_admin.html',encontrar_admin_inner)

def modificar_admin(request):
    def modificar_admin_inner(request):
        if request.method == "POST":
            id_admin = request.POST["id_admin"]
            admin_dj = get_object_or_404(Admin_django, id_admin=id_admin)
            nombre_admin = request.POST["nombre_admin"].strip()
            nivel_administrador = request.POST["nivel_administrador"].strip()
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
            if nivel_administrador != "":
                if nivel_administrador != admin_dj.nivel_administrador:
                    admin_dj.nivel_administrador = nivel_administrador
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
    return verificar_permisos_admin(request,3,'html/admindjango/modificar_admin.html',modificar_admin_inner)

def eliminar_admin(request, pk):
    def eliminar_admin_inner(request):
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
    return verificar_permisos_admin(request,3,'html/admindjango/admin_opc_admin.html',eliminar_admin_inner)

# Funciones Imagen
def opciones_imagen(request):
    def opciones_imagen_inner(request):
        imagen = Imagen.objects.all()
        context = {'imagen':imagen}
        return render(request, 'html/Imagen/opciones_imagen.html', context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 1 or admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/Imagen/opciones_imagen.html',opciones_imagen_inner)

def admin_imagen(request):
    def admin_imagen_inner(request):
        imagen = Imagen.objects.all()
        context = {'imagen':imagen}
        return render(request, 'html/Imagen/admin_imagen.html', context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 1 or admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/Imagen/admin_imagen.html',admin_imagen_inner)

def subir_imagen(request):
    def subir_imagen_inner(request):
        if request.method == "POST":
            imagen = request.FILES.get("imagen")
            descripcion_imagen = request.POST["descripcion_imagen"]
            if imagen and not descripcion_imagen.isspace():
                imagen_campos = {
                    "imagen": imagen,
                    "descripcion_imagen": descripcion_imagen
                }
                imagen_object = Imagen.objects.create(**imagen_campos)
                context = {'mensaje': '✔ Imagen guardada con éxito', 'imagen': imagen_object}
                return render(request, 'html/Imagen/subir_imagen.html', context)
            else:
                context = {'mensaje': '❌ Error: Debes completar todos los campos obligatorios'}
                return render(request, 'html/Imagen/subir_imagen.html', context)
        else:
            return render(request, 'html/Imagen/subir_imagen.html')
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 1 or admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/Imagen/subir_imagen.html',subir_imagen_inner)

def encontrar_imagen(request,pk):
    def encontrar_imagen_inner(request):
        if pk != " ":
            imagen = Imagen.objects.get(id_imagen=pk)
            context={'imagen':imagen}
        if imagen:
            return render(request,'html/Imagen/modificar_imagen.html',context)
        else:
            context={'mensaje':'❌ Error: ID de la imagen no encontrada'}
            return render(request,'html/Imagen/opciones_imagen.html',context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 1 or admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/Imagen/modificar_imagen.html',encontrar_imagen_inner)

def modificar_imagen(request):
    def modificar_imagen_inner(request):
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
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 1 or admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/Imagen/modificar_imagen.html',modificar_imagen_inner)

def eliminar_imagen(request, pk):
    def eliminar_imagen_inner(request):
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
            context = {'imagenes': imagenes, 'mensaje': '🤷 Error: ID de la imagen no encontrada'}
            return render(request, 'html/Imagen/opciones_imagen.html', context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 1 or admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/Imagen/opciones_imagen.html',eliminar_imagen_inner)

# Funciones Usuario
def opciones_usuario(request):
    def opciones_usuario_inner(request):
        usuario = Usuario.objects.all()
        context = {'usuario':usuario}
        return render(request, 'html/usuarios/opciones_usuario.html',context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/usuarios/opciones_usuario.html',opciones_usuario_inner)
    else:
        return verificar_permisos_admin(request,3,'html/usuarios/opciones_usuario.html',opciones_usuario_inner)

def admin_usuario(request):
    def admin_usuario_inner(request):
        usuario = Usuario.objects.all()
        context = {'usuario':usuario}
        return render(request, 'html/usuarios/admin_usuarios.html',context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/usuarios/admin_usuarios.html',admin_usuario_inner)
    else:
        return verificar_permisos_admin(request,3,'html/usuarios/opciones_usuario.html',admin_usuario_inner)

def crear_usuario(request):
    def crear_usuario_inner(request):
        if request.method == "POST":
            nombre_usuario = request.POST["nombre_usuario"].strip()
            correo_usuario = request.POST["correo_usuario"].strip()
            contrasena_usuario = request.POST["contrasena_usuario"].strip()
            confirmar_contrasena_usuario = request.POST["confirmar_contrasena_usuario"].strip()
            if not (nombre_usuario and correo_usuario and contrasena_usuario and confirmar_contrasena_usuario):
                context = {'mensaje': '❌ Error: Todos los campos son obligatorios'}
            elif contrasena_usuario == confirmar_contrasena_usuario:
                if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                    context = {'mensaje': '❌ Error: El nombre de usuario ya está en uso'}
                elif Usuario.objects.filter(correo_usuario=correo_usuario).exists():
                    context = {'mensaje': '❌ Error: El correo ingresado ya está en uso'}
                else:
                    MAX_NOMBRE_USUARIO_LENGTH = 40
                    MAX_CORREO_USUARIO_LENGTH = 50
                    MAX_CONTRASENA_USUARIO = 30
                    if len(nombre_usuario) > MAX_NOMBRE_USUARIO_LENGTH:
                        context = {'mensaje': f'❌ Error: El nombre de usuario debe tener como máximo {MAX_NOMBRE_USUARIO_LENGTH} caracteres'}
                    elif len(correo_usuario) > MAX_CORREO_USUARIO_LENGTH:
                        context = {'mensaje': f'❌ Error: El correo del usuario debe tener como máximo {MAX_CORREO_USUARIO_LENGTH} caracteres'}
                    elif len(contrasena_usuario) > MAX_CONTRASENA_USUARIO:
                        context = {'mensaje': f'❌ Error: La contraseña de usuario debe tener como máximo {MAX_CONTRASENA_USUARIO} caracteres'}
                    else:
                        campos_usuario = {
                            "nombre_usuario": nombre_usuario,
                            "correo_usuario": correo_usuario,
                            "contrasena_usuario": contrasena_usuario
                        }
                        usuario = Usuario.objects.create(**campos_usuario)
                        context = {'mensaje': '✔ Usuario creado con éxito', 'usuario': usuario}
            else:
                context = {'mensaje': '❌ Error: Las contraseñas deben ser iguales'}
            return render(request, 'html/usuarios/crear_usuario.html', context)
        else:
            return render(request, 'html/usuarios/crear_usuario.html')
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/usuarios/crear_usuario.html',crear_usuario_inner)
    else:
        return verificar_permisos_admin(request,3,'html/usuarios/opciones_usuario.html',crear_usuario_inner)

def encontrar_usuario(request,pk):
    def encontrar_usuario_inner(request):
        if pk != " ":
            usuario = Usuario.objects.get(id_usuario = pk)
            context = {'usuario':usuario}
        if usuario:
            return render(request,'html/usuarios/modificar_usuario.html',context)
        else:
            context={'mensaje':'❌ Error: ID del usuario no encontrado'}
            return render(request,'html/usuarios/admin_usuarios.html',context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/usuarios/modificar_usuario.html',encontrar_usuario_inner)
    else:
        return verificar_permisos_admin(request,3,'html/usuarios/opciones_usuario.html',encontrar_usuario_inner)

def modificar_usuario(request):
    def modificar_usuario_inner(request):
        if request.method == "POST":
            id_usuario = request.POST["id_usuario"]
            usuario = get_object_or_404(Usuario, id_usuario = id_usuario)
            nombre_usuario = request.POST["nombre_usuario"].strip()
            correo_usuario = request.POST["correo_usuario"].strip()
            contrasena_usuario = request.POST["contrasena_usuario"].strip()
            contrasena_nueva1 = request.POST["contrasena_nueva1"].strip()
            contrasena_nueva2 = request.POST["contrasena_nueva2"].strip()
            cambios_realizados = False
            mensaje = ''
            if nombre_usuario != "":
                if nombre_usuario != usuario.nombre_usuario.strip():
                    if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                        mensaje = '❌ Error: El nombre de usuario ya está en uso'
                    else:
                        usuario.nombre_usuario = nombre_usuario
                        cambios_realizados = True
            if correo_usuario != "":
                if correo_usuario != usuario.correo_usuario.strip():
                    if Usuario.objects.filter(correo_usuario=correo_usuario).filter():
                        mensaje = '❌ Error: El correo del usuario ya está en uso'
                    else:
                        usuario.correo_usuario = correo_usuario
                        cambios_realizados = True
            if contrasena_nueva1 != "" or contrasena_nueva2 != "":
                if contrasena_nueva1 != contrasena_usuario:
                    if contrasena_nueva1 == contrasena_nueva2:
                        usuario.contrasena_usuario = contrasena_nueva1
                        cambios_realizados = True
                    else:
                        mensaje = '❌ Error: Las contraseñas nuevas deben ser iguales'
                else:
                    mensaje = '❌ Error: La contraseña nueva no puede ser igual a la anterior'
            elif not cambios_realizados:
                mensaje = '❌ Error: No se ha realizado ningún cambio'
            if cambios_realizados:
                usuario.save()
                mensaje = '✔ Usuario actualizado con éxito'
            context = {'mensaje': mensaje, 'usuario': usuario}
            return render(request, 'html/usuarios/modificar_usuario.html', context)
        else:
            usuario = Usuario.objects.all()
            context = {'usuario':usuario}
            return render(request, 'html/usuarios/opciones_usuario.html',context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/usuarios/modificar_usuario.html',modificar_usuario_inner)
    else:
        return verificar_permisos_admin(request,3,'html/usuarios/opciones_usuario.html',modificar_usuario_inner)

def eliminar_usuario(request,pk):
    def eliminar_usuario_inner(request):
        context = {}
        try:
            usuario = Usuario.objects.get(id_usuario=pk)
            usuario.delete()
            usuarios_totales = Usuario.objects.all()
            context['usuarios_totales'] = usuarios_totales
            return render(request,'html/usuarios/opciones_usuario.html',context)
        except Usuario.DoesNotExist:
            usuario = Usuario.objects.all()
            context = {'usuario':usuario,'mensaje':'🤷 Error, id del usuario no encontrado'}
            return render(request,'html/usuarios/opciones_usuario.html',context)
    admin_id = request.session.get('admin_id')
    admin = Admin_django.objects.get(id_admin=admin_id)
    admin_nivel = admin.nivel_administrador
    if admin_nivel == 2 or admin_nivel == 3:
        return verificar_permisos_admin(request,admin_nivel,'html/usuarios/opciones_usuario.html',eliminar_usuario_inner)
    else:
        return verificar_permisos_admin(request,3,'html/usuarios/opciones_usuario.html',eliminar_usuario_inner)

# Funciones Contacto
# PENDIENTE
def opciones_contacto(request):
    contacto = Contacto.objects.all()
    context = {'contacto':contacto}
    return render(request,'html/contactos/opciones_contacto.html',context)

def admin_contacto(request):
    contacto = Contacto.objects.all()
    context = {'contacto':contacto}
    return render(request,'html/contactos/admin_contacto.html',context)

def encontrar_contacto(request, pk):
    if pk != " ":
        contacto = Contacto.objects.get(id_contacto = pk)
        context = {'contacto':contacto}
    if contacto:
        return render(request,'html/contactos/revisar_contacto.html',context)
    else:
        context = {'mensaje':'❌ Error, id del contacto no encontrado'}
        return render(request,'html/contactos/opciones_contacto.html',context)