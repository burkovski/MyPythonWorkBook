import pickle
tom_file = open("tom.pkl", "rb")
tom = pickle.load(tom_file)
tom_file.close()
tom['name'] = "Tom Hanks"
tom_file = open("tom.pkl", "wb")
pickle.dump(tom, tom_file)
tom_file.close()