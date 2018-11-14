import pickle
db_file = open("people-pickle", "rb")
db = pickle.load(db_file)
db_file.close()

db['sue']['pay'] *= 1.10
db['tom']['name'] = 'Tom Hanks'

db_file = open("people-pickle", "wb")
pickle.dump(db, db_file)
db_file.close()