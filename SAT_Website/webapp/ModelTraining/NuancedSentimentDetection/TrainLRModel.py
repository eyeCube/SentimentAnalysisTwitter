from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle

model = LogisticRegression(max_iter=1000)
data = pd.read_csv('test.csv')
x = data.iloc[:,2:]
y = pd.read_csv('NB_training_data.csv')['category']
print(y)
model.fit(x, y)

with open('LR.pickle', 'wb') as f:
    pickle.dump(model, f)
