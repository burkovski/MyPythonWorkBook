from initdata import bob, sue, tom
import pickle
for (key, record) in [('bob', bob), ('sue', sue), ('tom', tom)]:
    rec_file = open(key + '.pkl', 'wb')
    pickle.dump(record, rec_file)
    rec_file.close()