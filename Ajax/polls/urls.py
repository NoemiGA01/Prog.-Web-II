from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cargar-municipios/', views.cargar_municipios, name='cargar_municipios'),
]