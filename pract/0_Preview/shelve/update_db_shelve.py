from initdata import tom
import shelve
db = shelve.open("people-shelve")
sue = db['sue']
sue['pay'] = 50000
db['sue'] = sue
tom['name'] = "Tom Hanks"
db['tom'] = tom