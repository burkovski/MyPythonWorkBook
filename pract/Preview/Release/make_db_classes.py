import shelve
from initdata import Person, Manager

bob = Person("Bob Smith", 44)
sue = Person("Sue Jones", 47, 40000, "hardware")
tom = Manager(name="Tom Hanks", age=50, pay=50000)

db = shelve.open("class-shelve")
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()