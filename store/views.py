from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm, SearchForm


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_or_create_cart(request):
    """Get or create cart for authenticated or guest user."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


# ─── Pages ────────────────────────────────────────────────────────────────────

def home(request):
    featured_products = Product.objects.filter(is_featured=True, stock__gt=0)[:8]
    categories = Category.objects.all()[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    search_form = SearchForm(request.GET)
    selected_category = request.GET.get('category', '')
    query = request.GET.get('q', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if selected_category:
        products = products.filter(category__slug=selected_category)

    context = {
        'products': products,
        'categories': categories,
        'search_form': search_form,
        'selected_category': selected_category,
        'query': query,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related,
    }
    return render(request, 'store/product_detail.html', context)


# ─── Cart ─────────────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    context = {
        'cart': cart,
        'cart_items': items,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        quantity = int(request.POST.get('quantity', 1))

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.get_item_count(),
                'message': f'"{product.name}" added to cart.',
            })

        messages.success(request, f'"{product.name}" has been added to your cart.')
        return redirect(request.META.get('HTTP_REFERER', 'store:cart'))

    return redirect('store:product_list')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)

    # Security: make sure item belongs to this cart
    if item.cart == cart:
        item.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': str(cart.get_total()),
                'cart_count': cart.get_item_count(),
            })
        messages.success(request, 'Item removed from cart.')

    return redirect('store:cart')


def update_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id)
        cart = get_or_create_cart(request)

        if item.cart == cart:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                item.delete()
            else:
                item.quantity = quantity
                item.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'subtotal': str(item.get_subtotal()) if quantity >= 1 else '0',
                    'cart_total': str(cart.get_total()),
                    'cart_count': cart.get_item_count(),
                })

    return redirect('store:cart')


# ─── Checkout & Orders ────────────────────────────────────────────────────────

def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.get_total()
            order.save()

            # Create order items (snapshot products)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            # Decrement stock
            for item in cart_items:
                product = item.product
                product.stock = max(0, product.stock - item.quantity)
                product.save()

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f'Order #{order.id} placed successfully! Thank you.')
            return redirect('store:order_success', order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/order_history.html', {'orders': orders})
