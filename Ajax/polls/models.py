from django.db import models

# Create your models here.
class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, related_name='municipios', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre