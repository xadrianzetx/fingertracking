import cv2
import redis
from flask import Flask, Response, render_template
from handtracking import HandTracker


app = Flask(__name__)
r = redis.StrictRedis(host='192.168.1.108', port=6379)


def track():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    try:
        while True:
            _, frame = cap.read()

            frame = tracker.draw_sampling_area(frame)
            tracker.histogram(frame)
            _, coord = tracker.track(frame)

            yield coord

    except:
        cv2.destroyAllWindows()
        cap.release()


def event_stream():
    channel = r.pubsub()
    channel.subscribe('devices')

    for msg in channel.listen():
        yield 'data: {}\n\n'.format(msg)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
