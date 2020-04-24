from os import path
import pickle

model_path = path.join(path.dirname(__file__), 'NB.pickle')
vectorizer_path = path.join(path.dirname(__file__), 'vectorizer.pickle')
def predict_sentiment(tweets):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    tweets = vectorizer.transform(tweets)
    result = model.predict(tweets)
    return result
