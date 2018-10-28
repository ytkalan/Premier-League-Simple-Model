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

        sgd_model = SGDClassifier(max_iter=5000)
        sgd_model.fit(data, label)
        score = sgd_model.score(data, label)
        print('window = {0}, data from {1}, score : {2}'.format(window, year, score))