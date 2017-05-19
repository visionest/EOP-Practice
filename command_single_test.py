#!/usr/bin/env python

from PIL import Image, ImageOps
import numpy as np
import json
import configargparse
from os.path import splitext

# Total classes
NUM_CLASSES = 1001

# Image Extension
IMG_EXT = ['.jpg', '.jpeg', 'png']

# Command line
parser = configargparse.ArgParser()
parser.add('--image_file', dest='image_file', required=True)
parser.add('--frozen_model', dest='frozen_model', default='graph_data/frozen_inception_resnet_v2.pb')
parser.add('--label_file', dest='label_file', default='translate/result_imagenet1001.json')

args = vars(parser.parse_args())
sample_image = args['image_file']
frozen_model = args['frozen_model']
label_file = args['label_file']


# Check Imagefile
_, file_ext = splitext(sample_image)
if file_ext not in IMG_EXT:
	raise NameError(sample_image + ' is NOT an image file!')
else:
	import tensorflow as tf


# Load and convert label
label = open(label_file, 'r')
label = json.load(label)

# Image preprocessing
def img_preproc(img, central_fraction=0.875):
	central_fraction = 0.875
	one_side_fraction = (1 - central_fraction) / 2.0
	im = Image.open(sample_image)
	im = ImageOps.fit(im, (299, 299), method=2, bleed=one_side_fraction, centering=(0.5, 0.5)) # method > BILINEAR=2, NEAREST=0 (default)
	im = np.array(im).astype(dtype='float32')
	im = im.reshape(-1,299,299,3)
	im = 2*(im / 255.0) - 1.0
	return im

# Get Top5 infomations [0]:prob, [1]:index
def get_top5_with_idx(prob):
	prob_with_idx = zip(prob[0], range(NUM_CLASSES))
	prob_with_idx.sort()
	return prob_with_idx[NUM_CLASSES-5:]

# Load frozen model as graph
def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    
	with tf.Graph().as_default() as graph:
		tf.import_graph_def(
            graph_def, 
            input_map=None, 
            return_elements=None, 
            name="prefix", 
            op_dict=None, 
            producer_op_list=None
        )
    return graph

# Evaluation
def get_info(image):
	im = img_preproc(image)
	predict_values = sess.run(predictions, feed_dict={im_placeholder: im})
	return get_top5_with_idx(predict_values)

# Graph
graph = load_graph(frozen_model)
im_placeholder = graph.get_tensor_by_name('prefix/Placeholder:0')
predictions = graph.get_tensor_by_name('prefix/InceptionResnetV2/Logits/Predictions:0')
sess = tf.Session(graph=graph)

print "------------------------------------------------------------------------------------------"
print "File name : ", sample_image

print "------------------------------------------------"
print "------------------------------------------------"

result_info = get_info(sample_image)
for idx, i in enumerate(range(4, -1, -1)):
	print "TOP5 (predict value, index), (en_label), (kr_label) : #",idx+1, "-" , result_info[i], "(",label[str(result_info[i][1])].keys()[0],"), (",label[str(result_info[i][1])].values()[0],")"

print "------------------------------------------------------------------------------------------"
