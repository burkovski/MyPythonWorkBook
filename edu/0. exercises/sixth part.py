# # EX 1
# class Adder:
#     def __init__(self, data):
#         self.data = data
#     def __str__(self):
#         return "{}".format(self.data)
#     def __add__(self, other):
#         print("Not Implemented")
#
# class ListAdder(Adder):
#     def __init__(self, data=None):
#         if data is None:
#             data = []
#         Adder.__init__(self, data)
#     def __add__(self, x):
#         return ListAdder(self. data + x)
#
# class DictAdder(Adder):
#     def __init__(self, data=None):
#         if data is None:
#             data = {}
#         Adder.__init__(self, data)
#     def __add__(self, x):
#         res = self.data.copy()
#         res.update(x)
#         return DictAdder(res)
#
# L1 = [1, 2, 3]
# L2 = [4, 5]
# D1 = {'a': 1, 'b': 2}
# D2 = {'c': 3, 'd': 4, 'e': 5}
#
# X = ListAdder(L1)
# print(X + L2)
# Y = DictAdder(D1)
# print(Y + D2)
# print(L1, L2, D1, D2)
#


# # EX 2
# class MyList:
#     def __init__(self, val=None):
#         if val is None:
#             val = []
#         self.wrapped = [x for x in val]
#     def __str__(self):
#         return "MyList: {}".format(self.wrapped)
#     def __add__(self, other):
#         return MyList(self.wrapped + other)
#     def __mul__(self, other):
#         return MyList(self.wrapped * other)
#     def __getitem__(self, index):
#         return self.wrapped[index]
#     def __setitem__(self, offset, value):
#         self.wrapped[offset] = value
#     def __iter__(self):
#         self.offset = 0
#         return self
#     def __next__(self):
#         if self.offset == len(self.wrapped): raise StopIteration
#         item = self.wrapped[self.offset]
#         self.offset += 1
#         return item
#     def __contains__(self, item):
#         return item in self.wrapped
#     def __len__(self):
#         return len(self.wrapped)
#     def __getattr__(self, item):
#         return getattr(self.wrapped, item)
#     def append(self, x):
#         self.wrapped.append(x)
#     def sort(self):
#         self.wrapped.sort()
#
# L1 = [1, 2, 3]
# L2 = [4, 5]
# X = MyList(L1)
# print(X)
# print(X + L2)
# print(X * 2)
# print(X[:-1])
# for v in X:
#     print(v)
# X[:0] = [-x for x in reversed(X)] + [0]
# print(X)
# print(0 in X)
# print(len(X))
# X.reverse()
# print(X)


# EX. 4
# class Meta:
#     def __getattr__(self, item):
#         print("get:", item)
#     def __setattr__(self, key, value):
#         print("set: {0}={1}".format(key, value))
#
# x = Meta()
# x.append
# x.spam = 'pork'


# # EX 7
# class Lunch:
#     def __init__(self):
#         self.cust = Customer()
#         self.serv = Employee()
#     def order(self, food_name):
#         self.cust.placeOrder(food_name, self.serv)
#     def result(self):
#         self.cust.printFood()
#
# class Customer:
#     def __init__(self):
#         self.food = None
#     def placeOrder(self, food_name, employee):
#         self.food = employee.takeOrder(food_name)
#     def printFood(self):
#         print(self.food.name)
#
# class Employee:
#     def takeOrder(self, food_name):
#         return Food(food_name)
#
# class Food:
#     def __init__(self, name):
#         self.name = name
#
# x = Lunch()
# x.order("burritos")
# x.result()
# x.order("pizza")
# x.result()


# # EX 8
# class Animal:
#     def reply(self):
#         self.speak()
#     def speak(self):
#         print("spam")
#
# class Mammal(Animal):
#     def speak(self):
#         print("huh?")
#
# class Cat(Mammal):
#     def speak(self):
#         print("meow")
#
# class Dog(Mammal):
#     def speak(self):
#         print("bark")
#
# class Primate(Mammal):
#     def speak(self):
#         print("Hello world!")
#
# class Hacker(Primate):
#     pass
#
# x = Hacker()
# x.reply()