import os
import re
import pandas as pd

script_dir = os.path.dirname(__file__)
source_data = pd.read_csv('{0}{1}'.format(script_dir, 'data/results.csv'))

# Simplify Season Notation
source_data['season'] = source_data['season'].apply(lambda data: re.search(r'([0-9]+)', data).group(1))

dataframe_per_team = {}


# transform data to data by team
def data_transformation(row, home=True):
    data = {
        'mode': 'H' if home else 'A',
        'season': row['season'],
        'opponent': row['away_team'] if home else row['home_team'],
        'goal': row['home_goals'] if home else row['away_goals'],
        'concede': row['away_goals'] if home else row['home_goals'],
        'margin': (1 if home else -1) * (row['home_goals'] - row['away_goals']),
    }
    target_team = row['home_team'] if home else row['away_team']
    if target_team.replace(' ', '_') not in dataframe_per_team:
        dataframe_per_team[target_team.replace(' ', '_')] = []
    dataframe_per_team[target_team.replace(' ', '_')].append(data)


for index, row in source_data.iterrows():
    data_transformation(row, home=True)
    data_transformation(row, home=False)

for key in dataframe_per_team:
    pd.DataFrame(data=dataframe_per_team[key]).to_csv('transformed_data/{0}.csv'.format(key))
