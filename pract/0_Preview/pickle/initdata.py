# Записи
bob = dict(name="Bob Smith", age=42, pay=30000, job="dev")
sue = dict(name="Sue Jones", age=45, pay=40000, job="mgr")
tom = dict(name="Tom", age=50, pay=0, job=None)

# База данных
db = {}
db["bob"] = bob
db["sue"] = sue
db["tom"] = tom

if __name__ == "__main__":
    for key in db:
        print(key, '=>\n\t', db[key])