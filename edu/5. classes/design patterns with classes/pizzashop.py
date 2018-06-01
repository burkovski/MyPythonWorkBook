from employees import PizzaRobot, Server

class Customer:
    def __init__(self, name):
        self.name = name
    def order(self, server):
        print(self.name, "orders from", server)
    def pay(self, server):
        print(self.name, "pays for items to", server)

class Oven:
    def bake(self):
        print("Oven bakes")

class PizzaShop:
    def __init__(self):
        self.server = Server("Pat")     # Встроить другие объекты
        self.chef = PizzaRobot("Bob")   # Робот по имени Bob
        self.oven = Oven()

    def order(self, name):
        customer = Customer(name)
        customer.order(self.server)
        self.chef.work()
        self.oven.bake()
        customer.pay(self.server)


if __name__ == "__main__":
    scene = PizzaShop()
    scene.order("Homer")
    print("...")
    scene.order("Shaggy")