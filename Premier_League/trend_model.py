import os
import pickle
import csv

script_dir = os.path.dirname(__file__)
folder_dir = 'transformed_data'
window = 5

with open('{0}{1}/data_set'.format(script_dir, folder_dir), 'rb') as source_file:
    input_list = pickle.load(source_file)

usable_data = list(filter(lambda record: record['season'] > 2007, input_list))

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
