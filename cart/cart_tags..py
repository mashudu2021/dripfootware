# cart_tags.py

from django import template
from store.models import CartItem

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_item_count(context):
    request = context['request']
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        cart = Cart.objects.filter(user_profile=user_profile).first()
        if cart:
            return cart.cartitem_set.count()
    return 0
