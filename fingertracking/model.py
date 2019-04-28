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
        w, h, _ = frame.shape
        scaled_w = w // 2
        scaled_h = h // 2

        res_frame = cv2.resize(frame, (scaled_w, scaled_h), interpolation=cv2.INTER_AREA)
        rgb_frame = cv2.cvtColor(res_frame, cv2.COLOR_BGR2RGB)
        expanded = np.expand_dims(rgb_frame, axis=0)

        image_tensor = self._graph.get_tensor_by_name('image_tensor:0')
        dbox = self._graph.get_tensor_by_name('detection_boxes:0')
        dscore = self._graph.get_tensor_by_name('detection_scores:0')

        boxes, probas = self._sess.run([dbox, dscore], feed_dict={image_tensor: expanded})

        boxes = np.squeeze(boxes, axis=0)
        probas = np.squeeze(probas, axis=0)
        coords = [box for box, proba in zip(boxes, probas) if proba > 0.6]

        for c in coords:
            a = (int(c[1] * h), int(c[0] * w))
            b = (int(c[3] * h), int(c[2] * w))
            cv2.rectangle(frame, a, b, (0, 255, 0), 2, 1)

        return frame
