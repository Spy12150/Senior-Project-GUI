import tensorflow as tf
import numpy as np



model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(84),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1),
])


print(model.summary())
