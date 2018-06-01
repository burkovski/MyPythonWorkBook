registry = {}
def register(obj):
    registry[obj.__name__] = obj
    return obj

@register
def spam(x):
    return x * 2

@register
def ham(x):
    return x * 4

@register
class Eggs:
    def __init__(self, x):
        self.data = x * 8
    def __str__(self):
        return str(self.data)

print("Registry:")
for name in registry:
    print(name, "=>", registry[name], type(registry[name]))

print("\n Manual calls:")
print(spam(2))
print(ham(2))
print(Eggs(2))

print("\nRegistry calls:")
for name in registry:
    print(name, "=>", registry[name](3))


def annotate(text):
    def decorate(func):
        func.label = text
        return func
    return decorate

@annotate('spam data')
def spam(a, b):             # spam = annotate(...)(spam)
    return a + b

print(spam(1, 2), spam.label)