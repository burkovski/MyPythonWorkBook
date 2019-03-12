import shelve
from initdata import Person, Manager
field_names = ('name', 'age', 'job', 'pay')

db = shelve.open("class-shelve")

while True:
    key = input("\nKey? => ")
    if not key: break
    if key in db:
        record = db[key]
    else:
        record = Person(name='?', age='?')
    for field in field_names:
        curr_val = getattr(record, field)
        new_text = input("\t[{0}]={1}\n\t\tnew?=>".format(field, curr_val))
        if new_text:
            setattr(record, field, eval(new_text))
    db[key] = record
db.close()