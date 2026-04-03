from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Category, Product, Order, OrderItem


def home(request):
    categories = Category.objects.all()
    return render(request, 'catalog/home.html', {'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'catalog/category_list.html', {'categories': categories})


def product_list_by_category(request, slug):
    catalog_obj = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=catalog_obj, is_active=True)

    qs = qs.select_related('category').prefetch_related('images')

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass

    if request.GET.get('in_stock') == '1':
        qs = qs.filter(stock__gt=0)

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'new':
        qs = qs.order_by('-id')
    else:
        qs = qs.order_by('name')

    paginator = Paginator(qs, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)
    qs_params = params.urlencode()

    return render(request, 'catalog/product_list.html', {
        'catalog': catalog_obj,
        'page_obj': page_obj,
        'qs_params': qs_params,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock == 0:
        messages.error(request, 'Товар нет в наличии.')
        return redirect('catalog:product_detail', slug=product.slug)

    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    current_qty = cart.get(product_id_str, 0)

    if current_qty + 1 > product.stock:
        messages.error(request, f'Нельзя добавить больше {product.stock} шт.')
        return redirect('catalog:product_detail', slug=product.slug)

    cart[product_id_str] = current_qty + 1
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'{product.name} добавлен в корзину.')
    return redirect('catalog:product_detail', slug=product.slug)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        product = get_object_or_404(Product, id=product_id)
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product.name} удалён из корзины.')
    return redirect('catalog:cart_detail')


def increase_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    current_qty = cart.get(product_id_str, 0)

    if current_qty + 1 > product.stock:
        messages.error(request, f'Нельзя добавить больше {product.stock} шт.')
        return redirect('catalog:cart_detail')

    cart[product_id_str] = current_qty + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('catalog:cart_detail')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    current_qty = cart.get(product_id_str, 0)

    if current_qty > 1:
        cart[product_id_str] = current_qty - 1
    else:
        del cart[product_id_str]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('catalog:cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_sum = Decimal('0.00')
    total_quantity = 0
    positions = 0

    for product_id_str, qty in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str), is_active=True)
        item_total = product.price * qty
        cart_items.append({
            'product': product,
            'quantity': qty,
            'item_total': item_total,
        })
        total_sum += item_total
        total_quantity += qty
        positions += 1

    return render(request, 'catalog/cart_detail.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
        'positions': positions,
    })


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Корзина пуста.')
        return redirect('catalog:cart_detail')

    cart_items = []
    total_sum = Decimal('0.00')

    for product_id_str, qty in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str), is_active=True)
        if qty > product.stock:
            messages.error(request, f'Недостаточно товара {product.name} на складе.')
            return redirect('catalog:cart_detail')
        item_total = product.price * qty
        cart_items.append({
            'product': product,
            'quantity': qty,
            'item_total': item_total,
        })
        total_sum += item_total

    if request.method == 'POST':
        # Создать заказ
        order = Order.objects.create()
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            # Уменьшить stock
            item['product'].stock -= item['quantity']
            item['product'].save(update_fields=['stock'])

        # Привязать к пользователю
        if request.user.is_authenticated:
            order.user = request.user
            order.save(update_fields=['user'])

        # Очистить корзину
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, f'Заказ #{order.id} оформлен!')
        return redirect('catalog:home')

    return render(request, 'catalog/checkout.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catalog/my_orders.html', {'orders': orders})
