from trend_data_generator import TrendDataGenerator
from sklearn.linear_model import *

usable_year = [2013, 2014, 2015, 2016]
windows = [1, 2, 3, 4, 5]

for year in usable_year:
    for window in windows:
        label, data = TrendDataGenerator(
            read_from_raw_file = False,
            usable_year = year,
            window = window
        ).get_trend_data()

        lm_model = LogisticRegression(max_iter=5000, class_weight = "balanced")
        lm_model.fit(data, label)
        score = lm_model.score(data, label)
        print('window = {0}, data from {1}, score : {2}'.format(window, year, score))