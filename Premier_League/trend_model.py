import os
from os.path import isfile, join
import functools
import csv

script_dir = os.path.dirname(__file__)
folder_dir = 'transformed_data'

# data_files = [f for f in os.listdir('{0}{1}'.format(script_dir, folder_dir)) if isfile(join(script_dir, folder_dir, f))]
data_files = ['Arsenal', 'Manchester_United']
data_set = {}


def reduce_helper(tuple, accumulator):
    print(accumulator)
    print(tuple)
    accumulator[tuple[0]] = tuple[1]
    return accumulator


for file_name in data_files:
    data_set[file_name] = []
    with open('{0}{1}/{2}.csv'.format(script_dir, folder_dir, file_name), 'r') as source_file:
        csv_reader = csv.DictReader(source_file)
        for row in csv_reader:
            del row['']
            data_set[file_name].append(dict(row))


def trend_generator(data, window=5):
    for index in range(window, len(data)):
        win_track = 0
        lose_track = 0
        for window_index in range(0, window):
            win_track = (win_track + 1) if float(data[index - window + window_index]['margin']) > 0 else 0
            lose_track = (lose_track + 1) if float(data[index - window + window_index]['margin']) < 0 else 0
        data[index]['win_track'] = win_track
        data[index]['lose_track'] = lose_track


trend_generator(data_set['Arsenal'])
print(data_set['Arsenal'])
# trend_generator(data_set['Arsenal'])
# print(data_set['Arsenal'])


# print(manchester_united_data)
# print(arsenal_data)