import pickle
import numpy as np
from sklearn.linear_model import *
from trend_data_generator import TrendDataGenerator

# Get data from file
trend_data = TrendDataGenerator(
    read_from_raw_file = False,
    usable_year = 2015,
    window = 3
)
training_label, training_data = trend_data.get_trend_data()

# define and train model
lm_model = LogisticRegression(
    max_iter=50000,
    class_weight="balanced",
    solver="saga",
    multi_class="multinomial"
)
lm_model.fit(training_data, training_label)

match_to_predict = [
    ('Brighton and Hove Albion', 'Wolverhampton Wanderers'),
    ('Fulham', 'AFC Bournemouth'),
    ('Liverpool', 'Cardiff City'),
    ('Southampton', 'Newcastle United'),
    ('Watford', 'Huddersfield Town'),
    ('Leicester City', 'West Ham United'),
    ('Burnley', 'Chelsea'),
    ('Crystal Palace', 'Arsenal'),
    ('Manchester United', 'Everton'),
    ('Tottenham Hotspur', 'Manchester City'),
]

for home, away in match_to_predict:
    input_data = trend_data.get_prediction_meta(home = home, away = away)
    prediction = lm_model.predict([input_data])
    print('Home: {0:25s} Away: {1:25s} Prediction index: {2:10.8f}'.format(home, away, prediction[0]))


print()