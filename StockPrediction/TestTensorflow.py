import os
import keras
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print(keras.__version__)
print(tf.__version__)

test = tf.constant('test')
print(test)