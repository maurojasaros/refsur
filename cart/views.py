from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Cart, CartItem
from products.models import Product


#Agregar Carrito
@login_required
def add_to_cart(request, pk):

    producto = get_object_or_404(Product, pk=pk)

    # Obtener cantidad (default = 1)
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except ValueError:
        cantidad = 1

    if cantidad < 1:
        cantidad = 1

    # Validar stock general
    if producto.stock is not None and producto.stock <= 0:
        messages.error(request, "Sin stock disponible")
        return redirect('product_list')

    # Obtener o crear carrito
    cart, created = Cart.objects.get_or_create(
        usuario=request.user,
        estado='activo'
    )

    # Buscar si ya existe en carrito
    cart_item = CartItem.objects.filter(
        carrito=cart,
        producto=producto
    ).first()

    # 📦 SI YA EXISTE
    if cart_item:
        nueva_cantidad = cart_item.cantidad + cantidad

        if producto.stock is not None and nueva_cantidad > producto.stock:
            messages.error(request, "Stock insuficiente")
            return redirect('product_list')

        cart_item.cantidad = nueva_cantidad
        cart_item.save()

    # SI NO EXISTE
    else:
        if producto.stock is not None and cantidad > producto.stock:
            messages.error(request, "Stock insuficiente")
            return redirect('product_list')

        CartItem.objects.create(
            carrito=cart,
            producto=producto,
            cantidad=cantidad
        )

    messages.success(request, "Producto agregado al carrito")

    return redirect('product_list')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(usuario=request.user, estado='activo').first()

    if cart:
        items = CartItem.objects.filter(carrito=cart)

        
        for item in items:
            producto = item.producto

            if producto.stock is not None:
                
                if producto.stock <= 0:
                    item.delete()

                
                elif item.cantidad > producto.stock:
                    item.cantidad = producto.stock
                    item.save()

        #  recargar items actualizados
        items = CartItem.objects.filter(carrito=cart)

    else:
        items = []

    return render(request, 'products/cart.html', {
        'items': items,
        'cart': cart
    })

from django.views.decorators.http import require_POST

@require_POST
@login_required
def update_quantity(request, pk):
    item = get_object_or_404(CartItem, pk=pk, carrito__usuario=request.user)

    action = request.POST.get('action')

    if action == 'increase':
        if item.producto.stock is None or item.cantidad < item.producto.stock:
            item.cantidad += 1
            item.save()
        else:
            messages.error(request, "No hay más stock disponible")

    elif action == 'decrease':
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, carrito__usuario=request.user)
    item.delete()
    return redirect('view_cart')