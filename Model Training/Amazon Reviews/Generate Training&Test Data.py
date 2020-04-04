import pandas as pd
from sklearn.model_selection import train_test_split

DIR = r'C:/Users/okosa/Desktop/'
infile = DIR + 'sanitized.csv'
all_data = pd.read_csv(infile)

x_train, x_test, y_train, y_test = train_test_split(all_data['review_body'], all_data['star_rating'], test_size=.1)

training_data = pd.DataFrame()
training_data['review_body'] = x_train
training_data['star_rating'] = y_train

test_data = pd.DataFrame()
test_data['review_body'] = x_test
test_data['star_rating'] = y_test

training_data.to_csv(DIR + 'training_data.csv')
test_data.to_csv(DIR + 'test_data.csv')
