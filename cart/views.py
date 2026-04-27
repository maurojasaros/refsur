from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from django.contrib import messages

@login_required
def add_to_cart(request, pk):
    
    print("ADD TO CART REAL EJECUTÁNDOSE")

    producto = get_object_or_404(Product, pk=pk)

    
    if producto.stock is not None and producto.stock <= 0:
        messages.error(request, "Sin stock")
        return redirect('product_list')

    cart, created = Cart.objects.get_or_create(
        usuario=request.user,
        estado='activo'
    )

    cart_item = CartItem.objects.filter(
        carrito=cart,
        producto=producto
    ).first()

   
    if cart_item:
        if producto.stock is not None:
            updated = CartItem.objects.filter(
                pk=cart_item.pk,
                cantidad__lt=producto.stock  
            ).update(cantidad=F('cantidad') + 1)

            if updated == 0:
                return redirect('view_cart')  

        else:
            cart_item.cantidad += 1
            cart_item.save()

    
    else:
        if producto.stock is not None and producto.stock < 1:
            return redirect('product_list')

        CartItem.objects.create(
            carrito=cart,
            producto=producto,
            cantidad=1
        )

    return redirect('view_cart')

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

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, carrito__usuario=request.user)
    item.delete()
    return redirect('view_cart')