import pkg_resources
import tensorflow as tf


class HandTracker:

    def __init__(self):
        self._sess, self._graph = self._load_graph()

    def _load_graph(self):
        # model src
        # https://github.com/victordibia/handtracking/blob/master/model-checkpoint/ssdlitemobilenetv2/frozen_inference_graph.pb
        path = 'assets/ssd_mobilenetv2.pb'
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
        pass
