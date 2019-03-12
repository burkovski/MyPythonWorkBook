from initdata import db
import pickle
db_file = open("people-pickle", "wb")
pickle.dump(db, db_file)
db_file.close()