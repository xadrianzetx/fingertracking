import cv2
import pkg_resources
import tensorflow as tf


class HandTracker:

    def __init__(self, **kwargs):
        self._model = kwargs.get('model', default='ssd_mobilenetv2')
        self._sess, self._graph = self._load_graph()

    def _load_graph(self):
        # model src
        # https://github.com/victordibia/handtracking/blob/master/model-checkpoint/ssdlitemobilenetv2/frozen_inference_graph.pb
        path = 'assets/{}.pb'.format(self._model)
        abs_path = pkg_resources.resource_filename('fingertracking', path)
        graph = tf.Graph()

        with graph.as_default():
            gf = tf.gfile.GFile(abs_path, 'rb')
            g = gf.read()
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(g)
            tf.import_graph_def(graph_def)
            gf.close()

        return tf.Session(graph=graph_def), graph

    def track(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_tensor = self._graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = self._graph.get_tensor_by_name('detection_boxes:0')

        # TODO reshape before run
        bbox = self._sess.run([detection_boxes], feed_dict={image_tensor: rgb_frame})

        return bbox
