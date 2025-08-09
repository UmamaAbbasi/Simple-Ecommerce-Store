from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem
from .forms import RegisterForm
from .cart import Cart


# --------- Product Views ---------

def product_list(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        cart = Cart(request)
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product, quantity)
        return redirect('cart')

    return render(request, 'shop/product_detail.html', {'product': product})


# --------- Cart Views ---------



def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
        total += product.price * quantity

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })



@login_required
def remove_from_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    return redirect('cart')


# --------- Simple Mock Checkout --------

@login_required
def checkout(request):
    cart_items, total = get_cart_data(request)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # Create order
        order = Order.objects.create(user=request.user)
        
        # Save order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity']
            )

        # (Optional) store payment method in order model if you have a field for it
        # order.payment_method = payment_method
        # order.save()

        # Clear cart
        request.session['cart'] = {}

        # Pass payment method to confirmation
        request.session['payment_method'] = payment_method

        return redirect('order_confirmation')

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })



# --------- User & Auth Views ---------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})


def home_view(request):
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user) if request.user.is_authenticated else None

    register_form = RegisterForm()
    login_form = AuthenticationForm()

    return render(request, 'shop/home.html', {
        'products': products,
        'orders': orders,
        'register_form': register_form,
        'login_form': login_form,
    })


# --------- Dashboard View ---------

@login_required
def dashboard(request):
    # Fetch orders for the logged-in user
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'shop/dashboard.html', {'orders': orders})

def get_cart_data(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
        total += product.price * quantity

    return cart_items, total
@login_required
def order_confirmation(request):
    payment_method = request.session.pop('payment_method', None)
    return render(request, 'shop/order_confirmation.html', {'payment_method': payment_method})
