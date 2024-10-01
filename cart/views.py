from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def add_to_cart(request, product_id):
  
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')

    cart.add(product=product, quantity=quantity, size=size)

    response_data = {
        'message': 'Product added to cart successfully!',
        'cart_count': cart.__len__(),
        'cart_total': str(cart.calculate_total()),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)
    else:
        return redirect('cart:cart_summary')

@login_required
@require_POST
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')

    if quantity <= 0:
        cart.remove(product=product, size=size)
    else:
        cart.add(product=product, quantity=quantity, size=size)

    response_data = {
        'message': 'Cart updated successfully!',
        'cart_count': cart.__len__(),
        'cart_total': str(cart.calculate_total()),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)
    else:
        return redirect('cart:cart_summary')
    
@login_required
@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', None)
    cart.remove(product=product, size=size)

    response_data = {
        'message': 'Product removed from cart successfully!',
        'cart_count': cart.__len__(),
        'cart_total': str(cart.calculate_total()),
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)
    else:
        return redirect('cart:cart_summary')


def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    context = {
        'cart_items': cart_items,
        'subtotal': cart.get_cart_subtotal(),
        'tax': cart.calculate_tax(),
        'grand_total': cart.calculate_total(),
    }
    return render(request, 'cart_summary.html', context)
