from person import Person, Manager
import shelve

bob = Person("Bob Smith")                   # Создание объектов для сохранения
sue = Person("Sue Jones", job="dev", pay=100000)
tom = Manager("Tom Jones", 50000)

db = shelve.open("persondb")    # Имя хранилища
for object in (bob, sue, tom):  # В качестве ключа использовать атрибут name
    db[object.name] = object    # Сохранить объект в хранилище
db.close()                      # Закрыть после внесения изменений