import shelve
db = shelve.open("class-shelve")

sue = db["sue"]
sue.giveRaise(.10)
db["sue"] = sue

tom = db["tom"]
tom.giveRaise(.10)
db["tom"] = tom
db.close()