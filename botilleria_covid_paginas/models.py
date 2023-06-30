from django.db import models
# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=40, null=False)
    correo_usuario = models.CharField(max_length=50, null=False)
    contrasena_usuario = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre_usuario + ' - ' + self.correo_usuario
class Contacto(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('leido', 'Leído'),
        ('respondido', 'Respondido'),
    )
    id_contacto = models.AutoField(primary_key=True)
    nombre_contacto = models.CharField(max_length=40, null=False)
    correo_contacto = models.CharField(max_length=50, null=False)
    telefono_contacto = models.IntegerField(null=False)
    ciudad_contacto = models.CharField(max_length=40, null=False)
    mensaje_contacto = models.CharField(max_length=110, null=False)
    fecha_solicitud = models.DateField(null=False, auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return self.nombre_contacto + ' - ' + self.correo_contacto