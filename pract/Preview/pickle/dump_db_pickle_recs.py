import pickle, glob
for file_name in glob.glob('*.pkl'):
    rec_file = open(file_name,  'rb')
    record = pickle.load(rec_file)
    print(file_name, '=>\n', record)

sue_file = open("sue.pkl", "rb")
print(pickle.load(sue_file)['name'])