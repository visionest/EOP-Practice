#!/usr/bin/env python

import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

import configargparse
import os
from os.path import splitext

import json
import csv


# Allowed image extension
IMG_EXT = ['.jpg', '.png', '.jpeg', '.bmp']

# Total classes
NUM_CLASSES = 1001

# Command line
parser = configargparse.ArgParser()
parser.add('--image_dir', dest='image_dir', required=True)
parser.add('--batch_size', dest='batch_size', default=4, type=int)
parser.add('--save_csv', dest='csv_file', default='classification_results.csv')
parser.add('--frozen_model', dest='frozen_model', default='graph_data/frozen_inception_resnet_v2.pb')
parser.add('--label_file', dest='label_file', default='translate/result_imagenet1001.json')

# Command arguments
args = vars(parser.parse_args())
image_dir = args['image_dir']
batch_size = args['batch_size']
csv_file = args['csv_file']
frozen_model = args['frozen_model']
label_file = args['label_file']

# Load and convert label
label = open(label_file, 'r')
label = json.load(label)

# CSV UTF-8 Byte-Order-Mark
bom = open(csv_file, 'wb')
bom.write(bytearray(b'\xEF\xBB\xBF'))
bom.close()

# CSV format
result_csv = open(csv_file, 'ab')
field_names = ['directory', 'is_image', 'probability', 'index', 'kr_label']
result_writer = csv.DictWriter(result_csv, fieldnames=field_names)
result_writer.writeheader()

# Image preprocessing
def img_preproc(img, central_fraction=0.875):
	one_side_fraction = (1 - central_fraction) / 2.0
	im = Image.open(img)
        if im.mode != 'RGB':
            im = im.convert('RGB')
	im = ImageOps.fit(im, (299, 299), method=2 ,bleed=one_side_fraction, centering=(0.5, 0.5))
	im = np.array(im).astype(dtype='float32')
	im = 2*(im / 255.0) - 1.0
	return im

# Determine image is broken
def is_image(img_cond):
    try:
        Image.open(img_cond)
        return True
    except:
        return False

# Get Top5 with index infomations
def get_top5_with_idx(prob):
    top5_with_idx = []
    for x in range(prob.shape[0]):
        prob_with_idx = zip(prob[x], range(NUM_CLASSES))
        prob_with_idx.sort()
        top5_with_idx.append(prob_with_idx[NUM_CLASSES-5:])
    return top5_with_idx

# Evaluation
def get_info(im_batch):
    predict_values = sess.run(predictions, feed_dict={im_placeholder: im_batch})
    return get_top5_with_idx(predict_values)

# Get file name lists
def get_file_list(dir_path):
    img_list = []
    non_img_list = []
    broken_img_list = []
    for roots, _, files in os.walk(dir_path):
        for file_name in files:
            full_name = roots + '/' + file_name
            if is_image(full_name) == True:
                img_list.append(full_name)
            else:
                _, file_ext = splitext(file_name)
                if file_ext.lower() in IMG_EXT:
                    broken_img_list.append(full_name)
                else:
                    non_img_list.append(full_name)
    return img_list, non_img_list, broken_img_list

# Load frozen model
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

# Graph and session
graph = load_graph(frozen_model)
im_placeholder = graph.get_tensor_by_name('prefix/Placeholder:0')
predictions = graph.get_tensor_by_name('prefix/InceptionResnetV2/Logits/Predictions:0')
sess = tf.Session(graph=graph)

# Lists of image / non-image
images_list, non_images_list, broken_images_list = get_file_list(image_dir)
images_by_batch = [images_list[i:i+batch_size] for i in range(0, len(images_list), batch_size)]

print "--Main process start--"
# Image result
for batch in images_by_batch:
    preproc_batch_tmp = []

    for image in batch:
        preproc_batch_tmp.append(img_preproc(image))
    result_batch_info = get_info(preproc_batch_tmp)
    batch_len = len(batch)

    for k in range(batch_len):
        for j in range(4, -1, -1):
            if j == 4:
                result_writer.writerow({'directory':batch[k], 'is_image':'Yes', 'probability':result_batch_info[k][j][0], 'index':result_batch_info[k][j][1], 'kr_label':label[str(result_batch_info[k][j][1])].values()[0].encode('utf-8')})
            else:
                result_writer.writerow({'probability':result_batch_info[k][j][0], 'index':result_batch_info[k][j][1], 'kr_label':label[str(result_batch_info[k][j][1])].values()[0].encode('utf-8')})

# Non-image result
if len(non_images_list) != 0:
    for non_image in non_images_list:
        result_writer.writerow({'directory':non_image, 'is_image':'No'})

# Broken image result
if len(broken_images_list) != 0:
    for broken_image in broken_images_list:
        result_writer.writerow({'directory':broken_image, 'is_image':'Broken'})

print "--Process complete--"
