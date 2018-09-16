import os
import pickle
import csv
import pickle

script_dir = os.path.dirname(__file__)
folder_dir = 'transformed_data'
window = 5

with open('{0}{1}/data_set'.format(script_dir, folder_dir), 'rb') as source_file:
    input_list = pickle.load(source_file)

usable_data = list(filter(lambda record: record['season'] > 2012, input_list))

def get_head_to_head_record(index, target_team, opponent, window):
    related_record = [record for record in input_list if (
        record['target_team'] == target_team
        and record['opponent'] == opponent
        and record['index'] > index
    )]
    return sorted(related_record, key=lambda k: k['index'])[0: min(len(related_record), window)]

def get_team_momentum(index, target_team, window):
    related_record = [record for record in input_list if (
        record['target_team'] == target_team
        and record['index'] > index
    )]
    return sorted(related_record, key=lambda k: k['index'])[0: min(len(related_record), window)]

label = [record['margin'] for record in usable_data]
data = []

for record in usable_data:
    home_momentun = get_team_momentum(record['index'], record['target_team'], window)
    away_momentun = get_team_momentum(record['index'], record['opponent'], window)
    head_to_head = get_head_to_head_record(record['index'], record['target_team'], record['opponent'], window)

    home_record = sum([0] + [data['margin'] for data in home_momentun])
    home_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in home_momentun])
    
    away_record = sum([0] + [data['margin'] for data in away_momentun])
    away_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in away_momentun])

    head_to_head_record = sum([0] + [data['margin'] for data in head_to_head])
    head_to_head_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in head_to_head])

    massage_data = [
        int(home_record),
        int(home_margin),
        int(away_record),
        int(away_margin),
        int(head_to_head_record),
        int(head_to_head_margin),
    ]
    print('Calculating: {0}'.format(record['index']))
    data.append(massage_data)

with open('{0}{1}/{2}'.format(script_dir, 'trend', 'data'), 'wb') as f:
  pickle.dump(data, f)

with open('{0}{1}/{2}'.format(script_dir, 'trend', 'label'), 'wb') as f:
  pickle.dump(label, f)