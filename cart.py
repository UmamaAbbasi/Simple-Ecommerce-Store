class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def items(self):
        from .models import Product  # Local import to avoid circular dependency
        products = Product.objects.filter(id__in=self.cart.keys())
        return [
            {
                'product': product,
                'quantity': self.cart[str(product.id)],
                'total_price': product.price * self.cart[str(product.id)]
            }
            for product in products
        ]

    def get_total_price(self):
        return sum(item['total_price'] for item in self.items())

