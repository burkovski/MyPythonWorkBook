class C2: ...

class C3: ...

class C1(C2, C3):               # Создать класс С1
    def setname(self, who):     # присвоить С1.setname
        self.name = who         # self - либо I1, либо I2

I1 = C1()   # Создать два экземпляра класса С1
I2 = C1()

I1.setname("bob")   # Записать bob в I1.name
I2.setname("mel")   # Записать mel в I2.name
print(I1.name)      # Выведет: bob
del C1, I1, I2

class C1(C2, C3):
    def __init__(self, who):    # Создать имя при создании кдасса
        self.name = who         # self - либо I1, либо I2

I1 = C1("bob")      # Записать bob в I1.name
I2 = C1("mel")      # Записать mel в I2.name
print(I1.name)      # Выведет: bob