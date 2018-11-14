class Person:
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay += int(self.pay * percent)
    def __str__(self):
        return "<{0} => {1}: {2} {3}>".format(self.__class__.__name__,
                                            self.name,
                                            self.job,
                                            self.pay,)

class Manager(Person):
    def __init__(self, name, age, pay):
        super().__init__(name, age, pay, job="manager")
    def giveRaise(self, percent, bonus=0.10):
        super().giveRaise(percent + bonus)


if __name__ == '__main__':
    bob = Person("Bob Smith", 44)
    sue = Person("Sue Jones", 47, 40000, "hardware")
    tom = Manager(name="Tom Hanks", age=50, pay=50000)
    print(sue, sue.pay, sue.lastName())
    for obj in (bob, sue, tom):
        obj.giveRaise(.10)
        print(obj)