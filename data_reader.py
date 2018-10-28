import os
import re
import pickle
import pandas as pd

class DataReader():


    def __init__(self, read_from_raw_file = True):
        
        if not os.path.isdir('/'.join(['transformed_data'])):
            os.mkdir('/'.join(['transformed_data']))
        
        if (read_from_raw_file):
            self.source_data = pd.read_csv('/'.join(['data', 'results.csv']))
            self.__save_formatted_data()

    def __data_transformation(self, row, index, home=True):
        data = {
            'index': index,
            'target_team': row['home_team'] if home else row['away_team'], 
            'mode': 'H' if home else 'A',
            'season': int(row['season']),
            'opponent': row['away_team'] if home else row['home_team'],
            'goal': int(float(row['home_goals'] if home else row['away_goals'])),
            'concede': int(float(row['away_goals'] if home else row['home_goals'])),
            'margin': int((1 if home else -1) * (row['home_goals'] - row['away_goals'])),
        }
        return data

    def __save_formatted_data(self, name = 'training_data.p'):
        self.source_data['season'] = self.source_data['season'].apply(
            lambda data: re.search(r'([0-9]+)', data).group(1)
        )
        transformed_data = []
        for index, row in self.source_data.iterrows():
            print(index)
            print(row)
            inverted_index = self.source_data.shape[0] - index
            transformed_data.extend([
                self.__data_transformation(row, index=inverted_index*2, home=True),
                self.__data_transformation(row, index=(inverted_index*2-1), home=False)
            ])
        transformed_data = sorted(transformed_data[::-1], key=lambda k: k['index'], reverse=False)

        with open('/'.join(['transformed_data', name]), 'wb') as f:
            pickle.dump(transformed_data, f)

    def get_formatted_data(self, name = 'training_data.p'):
        with open('/'.join(['transformed_data', name]), 'rb') as f:
            transformed_data = pickle.load(f)
        return transformed_data
