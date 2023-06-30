# Generated by Django 4.2.2 on 2023-06-28 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botilleria_covid_paginas', '0002_contacto_estado'),
        ('admin_botilleria', '0003_delete_almacen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id_mensaje', models.AutoField(primary_key=True, serialize=False)),
                ('remitente', models.CharField(max_length=50)),
                ('asunto', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('contacto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botilleria_covid_paginas.contacto')),
            ],
        ),
    ]