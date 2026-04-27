from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem

def product_list(request):
    productos = Product.objects.all()
    return render(request, 'products/product_list.html', {'productos': productos})

def product_detail(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'producto': producto})

@login_required
def add_to_cart(request, pk):
    producto = get_object_or_404(Product, pk=pk)

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
    cart, created = Cart.objects.get_or_create(
        usuario=request.user,
        estado='activo'
    )

    items = CartItem.objects.filter(carrito=cart)

    return render(request, 'products/cart.html', {
        'items': items,
        'cart': cart
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'products/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'products/login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'products/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


from cart.models import CartItem
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, carrito__usuario=request.user)
    item.delete()
    return redirect('view_cart')


