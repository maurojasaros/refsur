from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

@login_required
def add_to_cart(request, pk):
    producto = get_object_or_404(Product, pk=pk)

    # usar "usuario" porque así está en el modelo
    #cart, created = Cart.objects.get_or_create(usuario=request.user)

    cart, created = Cart.objects.get_or_create(
        usuario=request.user,
        estado='activo'
)

    cart_item, created = CartItem.objects.get_or_create(
        carrito=cart,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not created:
        cart_item.cantidad += 1
        cart_item.save()

    return redirect('product_list')


@login_required
def view_cart(request):
    cart = Cart.objects.filter(usuario=request.user, estado='activo').first()

    if cart:
        items = CartItem.objects.filter(carrito=cart)
    else:
        items = []

    return render(request, 'products/cart.html', {
        'items': items,
        'cart': cart
    })

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, carrito__usuario=request.user)
    item.delete()
    return redirect('view_cart')