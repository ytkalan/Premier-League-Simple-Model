import os
import pickle
import csv
from data_reader import DataReader

script_dir = os.path.dirname(__file__)
folder_dir = 'transformed_data'

class TrendDataGenerator():
    
    def __init__(
        self,
        read_from_raw_file = True,
        usable_year = 2013,
        window = 3,
    ):
        source_data = DataReader(read_from_raw_file = read_from_raw_file).get_formatted_data()
        self.usable_data = list(filter(lambda record: record['season'] > usable_year, source_data))
        self.usable_record = list(filter(lambda record: record['season'] > (usable_year-2), source_data))
        self.window = window
        self.label, self.data = self.generate_trend_data()
    
    def __get_head_to_head_record(self, index, target_team, opponent, window):
        related_record = [record for record in self.usable_record if (
            record['target_team'] == target_team
            and record['opponent'] == opponent
            and record['index'] > index
        )]
        return sorted(related_record, key=lambda k: k['index'])[0: min(len(related_record), window)]

    def __get_team_momentum(self, index, target_team, window):
        related_record = [record for record in self.usable_record if (
            record['target_team'] == target_team
            and record['index'] > index
        )]
        return sorted(related_record, key=lambda k: k['index'])[0: min(len(related_record), window)]

    def generate_trend_data(self):
        label = [record['margin']/abs(record['margin']) if record['margin'] != 0 else 0 for record in self.usable_data]
        data = []

        for record in self.usable_data:
            data.append(
                self.get_prediction_meta(
                    record['target_team'],
                    record['opponent'],
                    record['index']
                )
            )

        return label, data

    def get_prediction_meta(self, home, away, index = 0):
        home_momentun = self.__get_team_momentum(index, home, self.window)
        away_momentun = self.__get_team_momentum(index, away, self.window)
        head_to_head = self.__get_head_to_head_record(index, home, away, self.window)

        home_record = sum([0] + [data['margin'] for data in home_momentun])
        home_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in home_momentun])
    
        away_record = sum([0] + [data['margin'] for data in away_momentun])
        away_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in away_momentun])

        head_to_head_record = sum([0] + [data['margin'] for data in head_to_head])
        head_to_head_margin = sum([0] + [data['margin']/abs(data['margin']) if data['margin'] != 0 else 0 for data in head_to_head])

        return [
            int(home_record),
            int(home_margin),
            int(away_record),
            int(away_margin),
            int(head_to_head_record),
            int(head_to_head_margin),
        ]

        
    def get_trend_data(self):
        return self.label, self.data
