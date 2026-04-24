from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('comprado', 'Comprado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f"Carrito {self.id}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.cartitem_set.all())


class CartItem(models.Model):
    carrito = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad
    

