class Item:
    def __init__(self,name,price,quantity=0) :
        self.name =name
        self.price =price
        self.quantity =quantity
    def calculate_total_price(self):
        return self.price * self.quantity

item1 = Item("Phone",100,5)


print(item1.calculate_total_price(),item1.name)

