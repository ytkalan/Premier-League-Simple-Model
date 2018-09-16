import pickle
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
folder_dir = 'trend'
window = 5

with open('{0}{1}/data'.format(script_dir, folder_dir), 'rb') as source_file:
    train_data = np.array(pickle.load(source_file), np.int32)

with open('{0}{1}/label'.format(script_dir, folder_dir), 'rb') as source_file:
    train_labels = pickle.load(source_file)

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

def build_model():
  model = keras.Sequential([
    keras.layers.Dense(64, activation=tf.nn.relu,
                       input_shape=(train_data.shape[1],)),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dense(1)
  ])

  optimizer = tf.train.RMSPropOptimizer(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae'])
  return model

model = build_model()
model.summary()

history = model.fit(train_data, train_labels, epochs=500,
                    validation_split=0.2, verbose=0,
                    callbacks=[PrintDot()])

print('\n')
test_predictions = model.predict(np.array([[-4, -5, 1, 1, -3, -3]]))
print(test_predictions)