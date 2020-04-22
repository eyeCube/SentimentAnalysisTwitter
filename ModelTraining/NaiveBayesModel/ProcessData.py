# Process tweet data to be used in the NB model
# Author: Kosar-Kosarewicz

import pandas as pd
import numpy as np

data = pd.read_csv(r'C:\Users\okosa\Desktop\trainingandtestdata\training.1600000.processed.noemoticon.csv', encoding='latin-1')  # read in data from csv
print(data.iloc[:,0].count())
data = data.iloc[:, [0, 5]] # Keep rating and tweet body, drop the other columns
data.columns = ['rating', 'tweet']
data['tweet'] = data['tweet'].str.lower() # make the tweets all lowercase
data['tweet'].replace(regex=True, inplace=True, to_replace=r'[^a-z\s]', value='') # Remove punctuation and numbers from reviews

np.save("processedData", data, allow_pickle=True) # Save sanitized data
