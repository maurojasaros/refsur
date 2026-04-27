from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from products.models import Product  # 👈 IMPORTANTE (arriba del archivo)
from django.db.models import F 



@login_required
def checkout(request):
    print("ENTRE AL CHECKOUT")
    if request.method != 'POST':
        return redirect('view_cart')  # seguridad

    cart = Cart.objects.get(usuario=request.user, estado='activo')
    items = CartItem.objects.filter(carrito=cart)

   
    for item in items:
        producto = Product.objects.get(pk=item.producto.pk)

        if producto.stock is not None:
            if producto.stock < item.cantidad:
                return redirect('view_cart')

    
    order = Order.objects.create(
        usuario=request.user,
        total=cart.total,
        estado='pendiente'
    )

  
    for item in items:
        producto = Product.objects.get(pk=item.producto.pk)

        OrderItem.objects.create(
            pedido=order,
            producto=producto,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )

        if producto.stock is not None:
            Product.objects.filter(pk=producto.pk).update(
                stock=F('stock') - item.cantidad
            )

            print("STOCK DESCONTADO (DB):", producto.nombre)  # 👈 DEBUG

   
    cart.estado = 'comprado'
    cart.save()

    return redirect('product_list')


@login_required
def my_orders(request):
    orders = Order.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, usuario=request.user)
    items = OrderItem.objects.filter(pedido=order)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items
    })
