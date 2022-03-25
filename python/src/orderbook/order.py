class Order:
    
    def __init__(self, id, price, quantity, is_buy, time):
        self.id = id
        self.price = price
        self.quantity = quantity
        self.unfilled_quantity = quantity
        self.is_buy = is_buy
        self.time = time

    def get_id(self):
        return self.id

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_unfilled_quantity(self):
        return self.unfilled_quantity
    
    def get_is_buy(self):
        return self.is_buy

    def get_time(self):
        return self.time

    def __str__(self):
        return "Order(id: {}, price: {}, quantity: {}, unfilled_quantity: {}, is_buy: {}, time: {})".format(
                self.id, self.price, self.quantity, self.unfilled_quantity, self.is_buy, self.time
            )
