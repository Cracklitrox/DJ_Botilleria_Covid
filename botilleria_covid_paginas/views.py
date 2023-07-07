from django.shortcuts import render, redirect
from admin_botilleria.models import Productos
from .models import Usuario
from django.db.models import Q
from functools import wraps

def obtener_usuario_contexto(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get("usuario_id")
        usuario = None
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id_usuario=usuario_id)
            except Usuario.DoesNotExist:
                pass
        return view_func(request, usuario, *args, **kwargs)
    return wrapper

@obtener_usuario_contexto
def index(request, usuario):
    return render(request, "index.html", {"usuario": usuario})

def cerrar_sesion(request):
    if "usuario_id" in request.session:
        del request.session["usuario_id"]
    return redirect("index")

@obtener_usuario_contexto
def cerveza(request, usuario):
    productos = Productos.objects.filter(imagen__icontains="cerveza")
    return render(
        request, "html/cerveza.html", {"productos": productos, "usuario": usuario}
    )

@obtener_usuario_contexto
def contacto(request, usuario):
    return render(request, "html/contacto.html", {"usuario": usuario})

@obtener_usuario_contexto
def productos(request, usuario):
    productos = Productos.objects.filter(
        Q(imagen__contains="cerveza")
        | Q(imagen__contains="vino")
        | Q(imagen__contains="whisky")
    )
    return render(
        request, "html/productos.html", {"productos": productos, "usuario": usuario}
    )

def reestablecer_contraseña(request):
    return render(request, "html/reestablecer_contraseña.html")

@obtener_usuario_contexto
def registro(request, usuario):
    if request.method == "POST":
        nombre_usuario = request.POST["name"]
        correo_usuario = request.POST["email"]
        contrasena_usuario = request.POST["password"]
        usuario = Usuario.objects.create(
            nombre_usuario=nombre_usuario,
            correo_usuario=correo_usuario,
            contrasena_usuario=contrasena_usuario,
        )
        return render(request, "html/inicio_sesion.html", {"usuario": usuario})
    else:
        return render(request, "html/registro.html")

@obtener_usuario_contexto
def inicio_sesion(request, usuario=None):
    if request.method == "POST":
        nombre_usuario = request.POST.get("login_field")
        correo_usuario = request.POST.get("login_field")
        contrasena = request.POST.get("password")
        usuario = Usuario.objects.filter(nombre_usuario=nombre_usuario, contrasena_usuario=contrasena).first()
        if usuario:
            request.session['usuario_id'] = usuario.id_usuario
            return redirect('index')
        usuario = Usuario.objects.filter(correo_usuario=correo_usuario, contrasena_usuario=contrasena).first()
        if usuario:
            request.session['usuario_id'] = usuario.id_usuario
            return redirect('index')
        return render(request, 'html/inicio_sesion.html')
    else:
        return render(request, 'html/inicio_sesion.html')

@obtener_usuario_contexto
def vinos(request, usuario):
    productos = Productos.objects.filter(imagen__icontains="vino")
    return render(
        request, "html/vinos.html", {"productos": productos, "usuario": usuario}
    )

@obtener_usuario_contexto
def whiskys(request, usuario):
    productos = Productos.objects.filter(imagen__icontains="whisky")
    return render(
        request, "html/whiskys.html", {"productos": productos, "usuario": usuario}
    )