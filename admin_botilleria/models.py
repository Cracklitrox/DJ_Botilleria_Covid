from django.db import models
from botilleria_covid_paginas.models import Usuario

# Create your models here.

class Admin_django(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre_admin = models.CharField(max_length=40, null=False)
    contrasena_admin = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre_admin

class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    titulo_producto = models.CharField(max_length=30, null=False)
    descripcion_producto = models.CharField(max_length=50, null=False)
    precio_producto = models.IntegerField(null=False)
    imagen = models.ImageField(null=False,verbose_name="Foto")
    informacion_adicional = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.titulo_producto + ' - ' + str(self.precio_producto)

class Almacen(models.Model):
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)

    def __str__(self):
        return str(self.id_producto) + ' = ' + str(self.cantidad)

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_usuario)

class Carrito_Productos(models.Model):
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField(null=False)

    def __str__(self):
        return str(self.id_producto) + ' = ' + str(self.cantidad_producto)

class Compras(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha_compra = models.DateField(null=False)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_compra) + ' = ' + str(self.id_usuario)

class Compras_Productos(models.Model):
    id_compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField(null=False)

    def __str__(self):
        return str(self.id_producto) + ' = ' + str(self.cantidad_producto)

class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField()
    descripcion_imagen = models.CharField(max_length=70)