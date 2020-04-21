# Process tweet data to be used in the NB model
# Author: Kosar-Kosarewicz

import pandas as pd
import numpy as np

data = pd.read_csv('fulldata.csv', encoding='latin-1')  # read in data from csv
data = data.iloc[:, [0, 5]] # Keep star rating and review body, drop the other columns
data.columns = ['rating', 'tweet']
data['tweet'] = data['tweet'].str.lower() # make the reviews all lowercase
data['tweet'].replace(regex=True, inplace=True, to_replace=r'[^a-z\s]', value='') # Remove punctuation and numbers from reviews

np.save("processedData", data, allow_pickle=True) # Save sanitized data
