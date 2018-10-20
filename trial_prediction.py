import pickle
import numpy as np
import os
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPClassifier
import trend_data_generator as data_scrapper

script_dir = os.path.dirname(__file__)
folder_dir = 'trend'

with open('{0}{1}/data'.format(script_dir, folder_dir), 'rb') as source_file:
    train_data = np.array(pickle.load(source_file), np.int32)

with open('{0}{1}/label'.format(script_dir, folder_dir), 'rb') as source_file:
    train_labels = np.array(pickle.load(source_file))

ridge_model = Ridge(alpha=10**-20, max_iter=50000)
ridge_model.fit(train_data, train_labels)

match_to_predict = [
    ('Chelsea', 'Manchester United'),
    ('AFC Bournemouth', 'Southampton'),
    ('Cardiff City', 'Fulham'),
    ('Manchester City', 'Burnley'),
    ('Newcastle United', 'Brighton and Hove Albion'),
    ('West Ham United', 'Tottenham Hotspur'),
    ('Wolverhampton Wanderers', 'Watford'),
    ('Huddersfield Town', 'Liverpool'),
    ('Everton', 'Crystal Palace'),
    ('Arsenal', 'Leicester City')
]

for home, away in match_to_predict:
    home_momentun = data_scrapper.get_team_momentum(0, home, 5)
    away_momentun = data_scrapper.get_team_momentum(0, away, 5)
    head_to_head = data_scrapper.get_head_to_head_record(0, home, away, 5)

    home_record = sum([0] + [data['margin'] for data in home_momentun])
    home_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in home_momentun])
    
    away_record = sum([0] + [data['margin'] for data in away_momentun])
    away_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in away_momentun])

    head_to_head_record = sum([0] + [data['margin'] for data in head_to_head])
    head_to_head_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in head_to_head])

    input_data = [
        int(home_record),
        int(home_margin),
        int(away_record),
        int(away_margin),
        int(head_to_head_record),
        int(head_to_head_margin),
    ]

    prediction = ridge_model.predict(np.array([input_data]))
    print('Home: {0:25s} Away: {1:25s} Prediction index: {2:10.8f}'.format(home, away, prediction[0]))


print()