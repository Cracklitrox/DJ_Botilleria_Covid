# Generated by Django 4.2.2 on 2023-07-11 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_botilleria', '0004_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_django',
            name='nivel_administrador',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
