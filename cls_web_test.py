import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import json


# Number of classes, Model, Label
NUM_CLASSES = 1001
FROZEN_MODEL = '../graph_data/frozen_inception_resnet_v2.pb'
LABEL_FILE = '../translate/result_imagenet1001.json'


class CLS:
    def __init__(self):
        self.graph = self.load_graph(FROZEN_MODEL)
        self.im_placeholder = self.graph.get_tensor_by_name('prefix/Placeholder:0')
        self.predictions = self.graph.get_tensor_by_name('prefix/InceptionResnetV2/Logits/Predictions:0')
        self.sess = tf.Session(graph=self.graph)
        self.label = open(LABEL_FILE, 'r')
        self.label = json.load(self.label)

    # Image preprocessing
    def img_preproc(self, im, central_fraction=0.875):
        one_side_fraction = (1 - central_fraction) / 2.0
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im = ImageOps.fit(im, (299, 299), method=2, bleed=one_side_fraction, centering=(0.5, 0.5))
        im = np.array(im).astype(dtype='float32')
        im = im.reshape(-1,299,299,3)
        im = 2*(im / 255.0) - 1.0
        return im

    # Get Top5 infomations
    def get_top5_with_idx(self, prob):
        prob_with_idx = zip(prob[0], range(NUM_CLASSES))
        prob_with_idx.sort()
        prob_with_idx = prob_with_idx[NUM_CLASSES-5:]
        top5_result = []
        for i in range(4, -1, -1):
            top5_result.append(
                    (prob_with_idx[i][0],
                    prob_with_idx[i][1],
                    self.label[str(prob_with_idx[i][1])].keys()[0],
                    self.label[str(prob_with_idx[i][1])].values()[0]
                    ) )
        return top5_result

    # Load frozen model
    def load_graph(self, frozen_graph_filename):
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
    def get_info(self, image):
        im = self.img_preproc(image)
        predict_values = self.sess.run(self.predictions, feed_dict={self.im_placeholder: im})
        return self.get_top5_with_idx(predict_values)

