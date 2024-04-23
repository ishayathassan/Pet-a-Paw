from django.shortcuts import render
from django.db.models import Q
from .models import Product


# Create your views here.

def shop_view(request):
    search_input = request.GET.get('searchInput', '')
    category_filter = request.GET.get('category', '')
    price_range_filter = request.GET.get('priceRange', '')
    sort_filter = request.GET.get('sort', '')

    products = Product.objects.filter(stock__gt=0)

    # if search_input:
    #     products = products.filter(name__icontains=search_input)
    if search_input:
        products = products.filter(
            Q(name__icontains=search_input) |
            Q(category__icontains=search_input)
        )

    if category_filter:
        products = products.filter(category=category_filter)

    if price_range_filter:
        min_price, max_price = map(int, price_range_filter.split('-'))
        products = products.filter(price__range=(min_price, max_price))

    if sort_filter:
        if sort_filter == 'name_asc':
            products = products.order_by('name')
        elif sort_filter == 'name_desc':
            products = products.order_by('-name')
        elif sort_filter == 'price_asc':
            products = products.order_by('price')
        elif sort_filter == 'price_desc':
            products = products.order_by('-price')

    total_products = products.count()

    context = {
        'products': products,
        'total_products': total_products,
    }
    return render(request, 'shop/shop.html', context=context)


def product_view(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'shop/product.html', context=context)
