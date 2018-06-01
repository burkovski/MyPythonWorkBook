class Super:
    def method(self):               # Поведение по умолчанию
        print("In Super.method")

    def delegate(self):
        self.action()               # Делегирование: ожидаемый метод

    def action(self):
        raise NotImplementedError("action must be defined!")


class Inheritor(Super):     # Наследует методы, ничего не переопределяет
    pass


class Replacer(Super):      # Полностью замещает method
    def method(self):
        print("in Replacer.method")


class Extend(Super):        # Расширяет поведение метода method
    def method(self):
        print("Starting Extend.method")
        Super.method(self)
        print("Ending Extend.method")


class Provider(Super):      # Определяет необходимый метод
    def action(self):
        print("In Provider.method")


if __name__ == "__main__":
    for class_ in (Inheritor, Replacer, Extend):
        print('\nclass {0}:..'.format(class_.__name__))
        class_().method()
    print("\nclass Provider:..")
    x = Provider()
    x.delegate()




