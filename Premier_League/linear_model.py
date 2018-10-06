import pickle
import numpy as np
import os
from sklearn.linear_model import Ridge, LassoLars, LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
folder_dir = 'trend'

with open('{0}{1}/data'.format(script_dir, folder_dir), 'rb') as source_file:
    train_data = np.array(pickle.load(source_file), np.int32)

with open('{0}{1}/label'.format(script_dir, folder_dir), 'rb') as source_file:
    train_labels = np.array(pickle.load(source_file))

def least_square_score(y_true, y_pred):
    error = 0
    for t, p in zip(y_true, y_pred):
        error += (t - p)**2
    return (error)

def get_cross_validation_score(model, X, y):
    kf = KFold(n_splits=4, random_state=None, shuffle=True)
    error = 0
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        model.fit(X_train, y_train)
        error += (least_square_score(model.predict(X_test), y_test)/len(y))**0.5
    return error

regularization = [10**i for i in range(-20, 15, 1)]
score = []

for r in regularization:
    lm_model = Ridge(alpha=r)
    score.append(get_cross_validation_score(lm_model, train_data, train_labels))

plt.subplot(221)
plt.plot(np.log10(regularization), score)
plt.title('Ridge')

score = []

for r in regularization:
    lm_model = LassoLars(alpha=r)
    score.append(get_cross_validation_score(lm_model, train_data, train_labels))

plt.subplot(222)
plt.plot(np.log10(regularization), score)
plt.title('LassoLars')

score = []

for r in regularization:
    lm_model = LogisticRegression(penalty='l2', C=r, max_iter=2000)
    score.append(get_cross_validation_score(lm_model, train_data, train_labels))

plt.subplot(223)
plt.plot(np.log10(regularization), score)
plt.title('Logistic Ridge')

score = []

for r in regularization:
    lm_model = LogisticRegression(penalty='l1', C=r, max_iter=2000)
    score.append(get_cross_validation_score(lm_model, train_data, train_labels))

plt.subplot(224)
plt.plot(np.log10(regularization), score)
plt.title('Logistic Lasso')

plt.show()
