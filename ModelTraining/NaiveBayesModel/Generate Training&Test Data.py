# Separate processed data into training, validation and testing data
# Author: Oscar Kosar-Kosarewicz

from sklearn.model_selection import train_test_split
import numpy as np

def generate_training_data(infile):
    all_data = np.load(infile, allow_pickle=True)

    x_train, x_test, y_train, y_test = train_test_split(all_data[:,1], all_data[:,0], test_size=.1, shuffle=True)
    x_val, x_test = np.array_split(x_train, 2)
    y_val, y_test = np.array_split(y_train, 2)

    training_data = np.column_stack([x_train, y_train])
    validation_data = np.column_stack([x_val, y_val])
    test_data = np.column_stack([x_test, y_test])
    return training_data, validation_data, test_data

if __name__ == '__main__':
    DIR = r'./'
    infile = DIR + 'processedData.npy'
    training_data, validation_data, test_data = generate_training_data(infile)
    np.save(DIR + 'training_data', training_data, allow_pickle=True)
    np.save(DIR + 'validation_data', validation_data, allow_pickle=True)
    np.save(DIR + 'test_data', test_data, allow_pickle=True)
