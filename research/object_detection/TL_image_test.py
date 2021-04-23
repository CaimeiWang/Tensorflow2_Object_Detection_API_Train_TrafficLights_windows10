
import numpy as np
import pandas as pd
import os
import six.moves.urllib as urllib
import sys
import tarfile
#import tensorflow as tf
import zipfile
import cv2
from collections import defaultdict
from io import StringIO
#from matplotlib import pyplot as plt
from PIL import Image

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



# # This is needed to display the images.
# %matplotlib inline

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# from utils import label_map_util
# from utils import visualization_utils as vis_util
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# What model to download.
#MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_NAME = 'TL_inference_graph'
#MODEL_FILE = MODEL_NAME + '.tar.gz'
#DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('TL_training', 'labelmap.pbtxt')

NUM_CLASSES =4

# download model
opener = urllib.request.URLopener()
# 下载模型，如果已经下载好了下面这句代码可以注释掉
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#tar_file = tarfile.open(MODEL_FILE)
# for file in tar_file.getmembers():
#     file_name = os.path.basename(file.name)
#     if 'frozen_inference_graph.pb' in file_name:
#         tar_file.extract(file, os.getcwd())

# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Helper code
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'TL_test'
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image ({}).jpg'.format(i)) for i in range(1, 3)]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        i=0
        data = pd.DataFrame()
        for image_path in TEST_IMAGE_PATHS:
            i=i+1
            image = Image.open(image_path)
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            width, height = image.size
            image_np = load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)
            s_boxes = boxes[scores > 0.02]
            s_classes = classes[scores > 0.02]
            s_scores = scores[scores > 0.02]

            for i in range(len(s_boxes)):
                ymin=s_boxes[i][0] * height  # ymin
                xmin= s_boxes[i][1] * width  # xmin
                ymax= s_boxes[i][2] * height  # ymax
                xmax= s_boxes[i][3] * width  # xmax

                cv2.rectangle(image_np,(int(xmin), int(ymin)),(int(xmax), int(ymax)),(255, 0, 0),2)
                if s_classes[i]==1:
                    TFclass='go'
                elif s_classes[i]==2:
                    TFclass='stop'
                elif s_classes[i]==3:
                    TFclass='ambiguous'
                elif s_classes[i]==4:
                    TFclass='warning'
                cv2.putText(image_np,TFclass, (int(xmin), int(ymax)+10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1e-3 * image_np.shape[0], (255, 0, 0),1)

            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            cv2.imshow('1.jpg',image_np)
            cv2.waitKey(0)
            cv2.destroyAllWindows()



            # plt.figure(figsize=IMAGE_SIZE)
            # plt.imsave('./TL_test'+str(i)+'.jpg',image_np)
            # plt.imshow(image_np)
            # plt.show()