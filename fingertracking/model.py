import cv2
import pkg_resources
import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import loader


class HandTracker:

    def __init__(self, **kwargs):
        self._model = kwargs.get('model', 'ssd_mobilenet')
        self._sess, self._graph = self._load_graph()

    def _load_graph(self):
        # src
        # https://github.com/victordibia/handtracking/blob/master/model-checkpoint/ssdlitemobilenetv2
        path = 'assets/{}/'.format(self._model)
        abs_path = pkg_resources.resource_filename('fingertracking', path)

        with tf.Graph().as_default() as graph:
            sess = tf.Session(graph=graph)
            loader.load(sess, [tf.saved_model.tag_constants.SERVING], abs_path)

        return sess, graph

    def track(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        expanded = np.expand_dims(rgb_frame, axis=0)

        image_tensor = self._graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = self._graph.get_tensor_by_name('detection_boxes:0')

        # TODO reshape before run
        bbox = self._sess.run(detection_boxes, feed_dict={image_tensor: expanded})

        return bbox
