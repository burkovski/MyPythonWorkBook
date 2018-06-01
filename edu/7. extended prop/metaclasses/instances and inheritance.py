class MetaOne(type):
    def __new__(mcs, cls_name, sprs, cls_dict):
        print("In MetaOne.new:", cls_name)
        return type.__new__(mcs, cls_name, sprs, cls_dict)
    @staticmethod
    def toast():
        print("toast")

class Super(metaclass=MetaOne):     # Объявление метакласса наследуется подклассами
    @staticmethod                   # MetaOne вызывается дважды при создании двух классов
    def spam():
        print("spam")

class Sub(Super):                   # Супер класс: наследование - не экземпляр
    @staticmethod                   # Классы наследуют атрибуты суперклассов
    def eggs():                     # Но не наследуют атрибуты метаклассов
        print("eggs")

X = Sub()
X.eggs()     # Наследует от класса Sub
X.spam()     # Наследует от класса Super
# X.toast()  # <- атрибуты метаклассов не наследуются