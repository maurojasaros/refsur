from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart.objects.get(usuario=request.user, estado='activo')
    items = CartItem.objects.filter(carrito=cart)

    order = Order.objects.create(
        usuario=request.user,
        total=cart.total,
        estado='pendiente'
    )

    for item in items:
        OrderItem.objects.create(
            pedido=order,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )

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
