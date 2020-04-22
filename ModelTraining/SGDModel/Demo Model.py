# Test the pickled model
import pickle
import pandas as pd

with open('vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)
with open('SGD.pickle', 'rb') as f:
    model = pickle.load(f)

while True:
    my_input = [[input('Enter text:')]]
    if my_input == [['q']]: break
    test_data = pd.DataFrame(my_input)
    test_data = test_data[0].str.lower()  # make the reviews all lowercase
    print(test_data)
    test_data.replace(regex=True, inplace=True, to_replace=r'[^a-z\s]',
                      value='')  # Remove punctuation and numbers from reviews
    test_data = vectorizer.transform(test_data)
    rating = model.predict(test_data)
    print('Score:', rating)
