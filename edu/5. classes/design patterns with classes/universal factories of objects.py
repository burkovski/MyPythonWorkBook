def factory(aClass, *args, **kwargs):   # Любое число позиционных и именованых аргументов
    return aClass(*args, **kwargs)

class Spam:
    @staticmethod
    def doit(massage):
        print(massage)

class Person:
    def __init__(self, name, job):
        self.name = name
        self.job = job

object1 = factory(Spam)                     # Создать экземпляр Spam
object2 = factory(Person, "Guido", "guru")  # Создать экземпляр Person