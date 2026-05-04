from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from products.models import Product
from django.db.models import F
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from django.contrib import messages

@login_required
def checkout(request):
    if request.method != 'POST':
        return redirect('view_cart')

    cart = Cart.objects.filter(usuario=request.user, estado='activo').first()

    if not cart:
        return redirect('view_cart')

    items = CartItem.objects.filter(carrito=cart)

    if not items.exists():
        return redirect('view_cart')

    # Validar stock SOLO para muebles
    for item in items:
        producto = item.producto

        if producto.tipo == 'mueble':
            if producto.stock is not None and producto.stock < item.cantidad:
                return redirect('view_cart')

    # Crear pedido
    order = Order.objects.create(
        usuario=request.user,
        total=cart.total,
        estado='pendiente'
    )

    # Crear items
    for item in items:
        OrderItem.objects.create(
            pedido=order,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )

    # TRANSBANK
    tx = Transaction(
        WebpayOptions(
            commerce_code="597055555532", #Lo consegui de la pagina de transbank developers
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", #Lo consegui de la pagina de transbank developers
            integration_type=IntegrationType.TEST
        )
    )

    response = tx.create(
        buy_order=str(order.id),
        session_id=str(request.user.id),
        amount=order.total,
        return_url="https://refsur.onrender.com/commit/"
    )

    # guardar pedido
    request.session['order_id'] = order.id

    # redirigir a Webpay
    return redirect(response['url'] + "?token_ws=" + response['token'])


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
    items = OrderItem.objects.filter(pedido=order)

    return render(request, 'orders/order_success.html', {
        'order': order,
        'items': items
    })

    

@login_required
def commit(request):
    token = request.GET.get("token_ws")

    if not token:
        messages.error(request, "❌ Error en la transacción (token inválido).")
        return redirect('my_orders')

    tx = Transaction(
        WebpayOptions(
            commerce_code="597055555532", #Lo consegui de la pagina de transbank developers
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", #Lo consegui de la pagina de transbank developers
            integration_type=IntegrationType.TEST
        )
    )

    response = tx.commit(token)

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id, usuario=request.user)

    # EVITAR DOBLE PROCESAMIENTO
    if order.estado == 'pagado':
        return redirect('order_success', pk=order.id)

    # VALIDACIÓN COMPLETA
    if (
        response.get('status') == 'AUTHORIZED' and
        str(response.get('buy_order')) == str(order.id) and
        int(response.get('amount')) == int(order.total)
    ):
        order.estado = 'pagado'

        items = OrderItem.objects.filter(pedido=order)

        for item in items:
            if item.producto.stock is not None:
                Product.objects.filter(pk=item.producto.pk).update(
                    stock=F('stock') - item.cantidad
                )

        cart = Cart.objects.filter(usuario=request.user, estado='activo').first()
        if cart:
            cart.estado = 'comprado'
            cart.save()

        order.save()

        messages.success(request, "✅ Pago realizado con éxito")

        return redirect('order_success', pk=order.id)

    else:
        order.estado = 'cancelado'
        order.save()

        messages.error(request, "❌ El pago fue rechazado o no coincide con la orden.")

        return redirect('payment_failed', pk=order.id)
    

@login_required
def payment_failed(request, pk):
    order = get_object_or_404(Order, pk=pk, usuario=request.user)
    return render(request, 'orders/payment_failed.html', {'order': order})