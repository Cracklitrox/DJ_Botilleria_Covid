# Generated by Django 4.2.2 on 2023-06-25 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_botilleria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
