'''
referenced by https://github.com/tensorflow/tensorflow/issues/7172
'''

import tensorflow as tf
import tensorflow.contrib.slim as slim
from inception_resnet_v2 import inception_resnet_v2, inception_resnet_v2_arg_scope
import numpy as np

'''
height = 299
width = 299
channels = 3
'''

# Create graph
X = tf.placeholder(tf.float32, shape=[None, 299, 299, 3])
with slim.arg_scope(inception_resnet_v2_arg_scope()):
    logits, end_points = inception_resnet_v2(X, num_classes=1001, is_training=False)
#predictions = end_points["Predictions"]
#saver = tf.train.Saver()

# Execute graph
with tf.Session() as sess:
    #saver.restore(sess, "inception_resnet_v2_2016_08_30.ckpt")
    tf.train.write_graph(sess.graph_def, './', 'inception_resnet_v2_2016_08_30.pbtxt')

print "--Process complete--"
