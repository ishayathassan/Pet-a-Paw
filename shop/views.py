from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, Cart, OrderDetails, OrderedProducts, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

def shop_view(request):
    search_input = request.GET.get('searchInput', '')
    category_filter = request.GET.get('category', '')
    price_range_filter = request.GET.get('priceRange', '')
    sort_filter = request.GET.get('sort', '')

    products = Product.objects.filter(stock__gt=0)

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

    if request.method == 'POST':
        if 'addToCart' in request.POST:
            if request.user.is_authenticated:
                product_id = request.POST.get('addToCart')
                user_id = request.user

                # Check if the product is already in the user's cart
                cart_item = Cart.objects.filter(user_id=user_id, product_id=product_id).first()

                if cart_item:
                    # If the product is already in the cart, increase the quantity by one
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    # If the product is not in the cart, add it to the cart with quantity 1
                    Cart.objects.create(user_id=user_id, product_id_id=product_id, quantity=1)

                return redirect('cart')  # Redirect to the cart page after adding to the cart
            else:
                messages.warning(request, "Please login before adding items to your cart.")
                return redirect('shop')  # Redirect back to the shop page if the user is not logged in

    context = {
        'products': products,
        'total_products': total_products,
    }
    return render(request, 'shop/shop.html', context=context)


def product_view(request, id):
    product = Product.objects.get(id=id)
    product_reviews = Review.objects.filter(product_id=id).order_by('-created_at')
    context = {'product': product, 'product_reviews': product_reviews}
    return render(request, 'shop/product.html', context=context)


@login_required
def cart_view(request):
    user_id = request.user
    cart_items = Cart.objects.filter(user_id=user_id)
    total = sum(item.product_id.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def confirm_payment(request):
    if request.method == 'POST':
        user_id = request.user
        cart_items = Cart.objects.filter(user_id=user_id)
        total = sum(item.product_id.price * item.quantity for item in cart_items)

        # Create a new order
        order = OrderDetails.objects.create(user_id=user_id, total=total)

        # Create ordered products
        for item in cart_items:
            OrderedProducts.objects.create(order_id=order, product_id=item.product_id, quantity=item.quantity)
            item.product_id.stock -= item.quantity
            item.product_id.save()

        # Clear the cart
        cart_items.delete()

        messages.success(request, "Payment confirmed. Your order has been placed successfully.")
        return redirect('cart')  # Redirect to the cart page or another page as needed

    messages.error(request, "Payment confirmation failed. Please try again.")
    return redirect('cart')  # Redirect to the cart page if not a POST request


@login_required
def update_cart(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('productId')
        user_id = request.user

        cart_item = Cart.objects.filter(user_id=user_id, product_id=product_id).first()
        if action == 'delete':
            if cart_item:
                product_name = cart_item.product_id.name  # Get the name of the product being deleted
                cart_item.delete()
                messages.success(request, f"{product_name} has been removed from your cart.")
        elif action == 'updateQuantity':
            new_quantity = request.POST.get('newQuantity', 0)
            modify = request.POST.get('modify', '')

            if cart_item:
                product = get_object_or_404(Product, pk=product_id)
                if modify == 'increase':
                    # Check if the available stock is enough to increase the quantity
                    if product.stock >= cart_item.quantity + 1:
                        cart_item.quantity += 1
                    else:
                        messages.warning(request, f"No more {product.name} left in stock.")
                elif modify == 'decrease':
                    cart_item.quantity = max(1, cart_item.quantity - 1)
                else:
                    # Check if the requested quantity doesn't exceed available stock
                    requested_quantity = int(new_quantity)
                    if requested_quantity <= product.stock:
                        cart_item.quantity = requested_quantity
                    else:
                        messages.warning(request, f"No more {product.name} left in stock.")

                cart_item.save()

    return redirect('cart')


@login_required
def submit_review(request, id):
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('reviewText')
        rating = int(request.POST.get('rating'))

        # Retrieve the product instance
        product = get_object_or_404(Product, id=id)

        review = Review(user=user, product=product, text=text, rating=rating)
        review.save()

    return redirect('single_product', id=id)

# def display_reviews(request, product_id):
#     product_reviews = Review.objects.filter(product_id=product_id)
#     context = {'product_reviews': product_reviews}
#     return render(request, 'shop/product_reviews.html', context=context)
