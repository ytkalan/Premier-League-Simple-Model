from trend_data_generator import TrendDataGenerator
from sklearn.linear_model import *
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd

years=[2012, 2013, 2014, 2015, 2016]
windows=[1, 2, 3, 4, 5]

for year in years:
    for window in windows:
        label, data_5 = TrendDataGenerator(
            read_from_raw_file=False,
            usable_year=year,
            window=5
        ).get_trend_data()

        label, data_4 = TrendDataGenerator(
            read_from_raw_file=False,
            usable_year=year,
            window=4
        ).get_trend_data()

        data = [a+b for a,b in list(zip(data_4, data_5))]

        parameters = {	
            'penalty': ['l2'],
            'tol' : [1e-4, 1e-5, 1e-8],
            'C': [0.05, 0.2, 0.5, 1],
            'solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
            'warm_start': [True, False]
        }

        lm_model = LogisticRegression(multi_class='multinomial', max_iter=5000)

        grid_logistic = GridSearchCV(lm_model, parameters, cv=5)
        grid_logistic.fit(data, label)

        pd.DataFrame(grid_logistic.cv_results_).sort_values(by='rank_test_score').to_csv('Logistic-{0}-{1}.csv'.format(year, window))