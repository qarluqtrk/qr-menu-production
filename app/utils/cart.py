from app.utils.poster import poster


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    # def add(self, product_id, quantity):
    #     product_id = str(product_id)
    #     if product_id not in self.cart:
    #         self.cart[product_id] = {'quantity': 0}
    #     self.cart[product_id]['quantity'] += quantity
    #     self.save()

    def add(self, product_id, modification_id=None, quantity=1):
        productID = str(product_id)
        if productID not in self.cart:
            self.cart[productID] = {'quantity': 0, 'modification_id': 0}

        self.cart[productID]['quantity'] += 1

        if modification_id:
            self.cart[productID]['modification_id'] = int(modification_id)
        self.save()

    def quantity_change(self, product_id, change_method):
        productID = str(product_id)
        if productID in self.cart:
            if change_method == 'plus':
                self.cart[productID]['quantity'] += 1
            elif change_method == 'minus':
                self.cart[productID]['quantity'] -= 1
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.cart = {}
        self.save()

    def get_cart(self):
        return self.cart

    def get_total_price(self):
        total = 0
        for product_id, item in self.cart.items():
            if item["modification_id"] == 0:
                product = poster.get_product(product_id)
                total += int(product['sources'][0]['price']) * int(item['quantity'])
            else:
                product = poster.get_product(product_id)
                try:
                    if product["modifications"]:
                        for modification in product["modifications"]:
                            if int(modification['modificator_id']) == int(item["modification_id"]):
                                total += int(modification['sources'][0]['price']) * int(item['quantity'])
                                break
                except:
                    if product["group_modifications"]:
                        for modification in product["group_modifications"][0]["modifications"]:
                            if modification['dish_modification_id'] == int(item["modification_id"]):
                                price = str(modification['price']) + "00"
                                total += int(price) * int(item['quantity'])
                                break
        return total
