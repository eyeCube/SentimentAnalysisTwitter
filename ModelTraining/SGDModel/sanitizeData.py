import string
import pandas as pd
import os

os.chdir('/home/okosa/sanitizeData/') # Change working directory to data file's directory
data = pd.read_csv('amazon_reviews_us_Camera_v1_00.tsv', delimiter='\t', error_bad_lines=False) # read in data from tsv
data = data[['star_rating', 'review_body']] # Keep star rating and review body, drop the other columns
data['review_body'] = data['review_body'].str.lower() # make the reviews all lowercase
data['review_body'].replace(regex=True, inplace=True, to_replace=r'[^a-z\s]', value='') # Remove punctuation and numbers from reviews
data.to_csv("sanitized.csv") # Save sanitized data to csv
