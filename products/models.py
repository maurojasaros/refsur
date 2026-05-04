from django.db import models

class Category(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Product(models.Model):
    TYPE_CHOICES = [
        ('casa', 'Casa'),
        ('mueble', 'Mueble'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TYPE_CHOICES)

    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)

    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    # CASA
    m2 = models.IntegerField(null=True, blank=True)
    planos = models.FileField(upload_to='planos/', null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)

    # MUEBLE
    stock = models.IntegerField(null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre