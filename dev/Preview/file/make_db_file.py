import sys

db_filename = 'people-file'
ENDDB = 'ENDDB.'
ENDREC = 'ENDREC.'
RECSEP = '=>'

def storeDbase(db, db_filename=db_filename):
    sys.stdout = open(db_filename, 'w')
    for key in db:
        print(key)
        for (name, value) in db[key].items():
            print(name + RECSEP + repr(value))
        print(ENDREC)
    print(ENDDB)
    sys.stdout = sys.__stdout__

def loadDbase(db_filename=db_filename):
    sys.stdin = open(db_filename)
    db = {}
    key = input()
    while key != ENDDB:
        rec = {}
        field = input()
        while field != ENDREC:
            name, value = field.split(RECSEP)
            rec[name] = eval(value)
            field = input()
        db[key] = rec
        key = input()
    return db

if __name__ == "__main__":
    from initdata import db
    storeDbase(db)

