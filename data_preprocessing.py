import os
import re
import pickle
import pandas as pd
from pymongo import MongoClient
from pymongo import errors

script_dir = os.path.dirname(__file__) 
source_data = pd.read_csv('{0}{1}'.format(script_dir, 'data/results.csv'))

db_name = 'premier'
collection_name = 'transformed_data'

client = MongoClient('localhost', 27017)

db = client[db_name]
collection = db[collection_name]

# Simplify Season Notation
source_data['season'] = source_data['season'].apply(lambda data: re.search(r'([0-9]+)', data).group(1))

transformed_data = []

def check_db_exists():
    try:
        client.server_info()
        return True
    except errors.ServerSelectionTimeoutError as err:
        return False
db_exists = check_db_exists()

# transform data to data by team
def data_transformation(row, index, home=True):
    data = {
        '_id' :index,
        'index': index,
        'target_team': row['home_team'] if home else row['away_team'], 
        'mode': 'H' if home else 'A',
        'season': int(row['season']),
        'opponent': row['away_team'] if home else row['home_team'],
        'goal': int(float(row['home_goals'] if home else row['away_goals'])),
        'concede': int(float(row['away_goals'] if home else row['home_goals'])),
        'margin': int((1 if home else -1) * (row['home_goals'] - row['away_goals'])),
    }
    transformed_data.append(data)
    if db_exists:
        collection.save(data)

for index, row in source_data.iterrows():
    inverted_index = source_data.shape[0] - index
    data_transformation(row, index=inverted_index*2, home=True)
    data_transformation(row, index=(inverted_index*2-1), home=False)

transformed_data = sorted(transformed_data[::-1], key=lambda k: k['index'], reverse=False)

with open('{0}{1}/data_set'.format(script_dir, 'transformed_data'), 'wb') as f:
  pickle.dump(transformed_data, f)
