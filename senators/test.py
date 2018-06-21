import pickle

with open('topics.pickle', 'rb') as f:
    topics = pickle.load(f)
    print(topics)
