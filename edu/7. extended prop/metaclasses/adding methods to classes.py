# Расширение с помощью метакласса - лучше поддерживает изменения в будущем
def eggsfunc(obj):
    return obj.value * 4

def hamfunc(obj, value):
    return value + "&ham"

class Extender(type):
    def __new__(mcs, cls_name, sprs, cls_dict):
        cls_dict["eggs"] = eggsfunc
        cls_dict["ham"] = hamfunc
        return type.__new__(mcs, cls_name, sprs, cls_dict)

class Client1(metaclass=Extender):
    def __init__(self, value):
        self.value = value
    def spam(self):
        return self.value * 2

class Client2(metaclass=Extender):
    value = "ni?"

X = Client1("Ni!")
print(X.spam())
print(X.eggs())
print(X.ham("bacon"))
Y = Client2()
print(Y.eggs())
print(Y.ham("bacon"))


# Расширение с помощью декоратора: реализует те же действия, что и метод __init__ метакласса
def Extender(aClass):
    aClass.eggs = eggsfunc
    aClass.ham = hamfunc
    return aClass

@Extender
class Client1:
    def __init__(self, value):
        self.value = value
    def spam(self):
        return self.value * 2

@Extender
class Client2:
    value = "ni?"

X = Client1("Ni!")
print(X.spam())
print(X.eggs())
print(X.ham("bacon"))
Y = Client2()
print(Y.eggs())
print(Y.ham("bacon"))