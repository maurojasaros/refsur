from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from products.models import Product
from django.db.models import F
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@login_required
def checkout(request):
    print("ENTRE AL CHECKOUT")

    if request.method != 'POST':
        return redirect('view_cart')

    # 🛒 Obtener carrito
    cart = Cart.objects.filter(usuario=request.user, estado='activo').first()

    if not cart:
        return redirect('view_cart')

    items = CartItem.objects.filter(carrito=cart)

    if not items.exists():
        return redirect('view_cart')

    # 🔍 Validar stock
    for item in items:
        producto = Product.objects.get(pk=item.producto.pk)

        if producto.stock is not None and producto.stock < item.cantidad:
            return redirect('view_cart')

    # 🧾 Crear pedido
    order = Order.objects.create(
        usuario=request.user,
        total=cart.total,
        estado='pendiente'
    )

    # 📦 Crear items + descontar stock
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

    # 📧 EMAIL PRO (HTML)
    subject = "Confirmación de compra"

    html_content = render_to_string('emails/order_email.html', {
        'user': request.user,
        'order': order
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body="",  # texto plano opcional
        from_email='noreply@refsur.cl',
        to=[request.user.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)

    # 🔒 Cerrar carrito
    cart.estado = 'comprado'
    cart.save()

    return redirect('order_success', pk=order.id)


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


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, usuario=request.user)
    return render(request, 'orders/order_success.html', {'order': order})