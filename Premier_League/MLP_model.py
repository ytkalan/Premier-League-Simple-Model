import pickle
import numpy as np
import os
from sklearn.decomposition import PCA
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
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
        pca = PCA(n_components=2)
        transformed_data = pca.fit_transform(X_train)
        model.fit(transformed_data, y_train)
        error += least_square_score(model.predict(pca.transform(X_test)), y_test)
    error = (error/len(y))**0.5
    return error

regularization = [10**i for i in range(-5, 5, 3)]
score = []

# for r in regularization:
#    mlp_model = MLPClassifier(alpha=r, learning_rate="adaptive", max_iter=2000)
# #    mlp_model = svm.SVC(gamma=0.00001, C=r, kernel='sigmoid')
#    score.append(get_cross_validation_score(mlp_model, train_data, train_labels))

# plt.plot(np.log10(regularization), score)
# plt.title('Ridge')

# plt.show()

mlp_model = MLPClassifier(alpha=10, learning_rate="adaptive", max_iter=2000)
mlp_model.fit(train_data, train_labels)
print(mlp_model.predict([[-4, -5, 1, 1, -3, -3]]))
