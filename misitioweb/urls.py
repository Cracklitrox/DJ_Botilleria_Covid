from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('botilleria_covid_paginas.urls')),
    path('', include('admin_botilleria.urls'))
]
