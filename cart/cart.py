from django.shortcuts import get_object_or_404
from store.models import Product
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, size=None):
        product_id = str(product.id)
        item_id = f"{product_id}_{size}" if size else product_id
        
        if item_id in self.cart:
            # Update quantity
            self.cart[item_id]['quantity'] += quantity
        else:
            self.cart[item_id] = {
                'quantity': quantity,
                'price': str(product.price),
                'size': size,
            }

        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def remove(self, product, size=None):
        product_id = str(product.id)
        item_id = f"{product_id}_{size}" if size else product_id
        
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def get_cart_items(self):
        cart_items = []
        for item_id, item_data in self.cart.items():
            # Handle item_id with or without size
            parts = item_id.split('_', 1)
            product_id = parts[0]
            size = parts[1] if len(parts) > 1 else None
            
            product = get_object_or_404(Product, pk=product_id)
            item_price = Decimal(item_data['price'])
            item_quantity = item_data['quantity']
            item_subtotal = item_price * item_quantity

            cart_items.append({
                'product': product,
                'size': size,
                'quantity': item_quantity,
                'subtotal': item_subtotal,
            })

        return cart_items

    def get_cart_quantity(self):
        return sum(item_data['quantity'] for item_data in self.cart.values())

    def get_cart_subtotal(self):
        subtotal = Decimal('0.00')
        for item_data in self.cart.values():
            item_price = Decimal(item_data['price'])
            item_quantity = item_data['quantity']
            subtotal += item_price * item_quantity
        return subtotal

    def calculate_tax(self):
        tax_rate = Decimal('0.15')
        subtotal = self.get_cart_subtotal()
        return subtotal * tax_rate

    def calculate_total(self):
        subtotal = self.get_cart_subtotal()
        tax = self.calculate_tax()
        return subtotal + tax
