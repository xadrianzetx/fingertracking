import cv2
import json
import redis
from flask import Flask, Response, render_template
from fingertracking import FingerTracker, HandTracker, Device


app = Flask(__name__)
r = redis.StrictRedis(host='192.168.1.108', port=6379)


def select():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    fl = 0
    fr = 0
    hover = False
    hitbox = 'hitbox_0'

    try:
        while True:
            _, frame = cap.read()
            _, coords = tracker.track(frame)

            h, w, _ = frame.shape
            hl = (0, (w // 2) - 80)
            hr = ((w // 2) + 80, w)

            if len(coords) > 0:
                x = coords[0][0]

                if hl[0] < x < hl[1]:
                    fl += 1
                    hover = True
                    hitbox = 'hitbox_l'

                elif hr[0] < x < hr[1]:
                    fr += 1
                    hover = True
                    hitbox = 'hitbox_r'

                else:
                    fl = 0
                    fr = 0
                    hover = False
                    hitbox = 'hitbox_0'

            data = {'fl': fl, 'fr': fr, 'hover': hover, 'hitbox': hitbox}
            payload = json.dumps(data)

            yield 'data: {}\n\n'.format(payload)

    except GeneratorExit:
        cv2.destroyAllWindows()
        cap.release()


def track():
    cap = cv2.VideoCapture(0)
    tracker = FingerTracker()

    devices = [
        Device('device_0', r),
        Device('device_1', r),
        Device('device_2', r)
    ]

    try:
        while True:
            _, frame = cap.read()

            frame = tracker.draw_sampling_area(frame)
            tracker.histogram(frame)
            _, coord = tracker.track(frame, devices)

            yield 'data: {}\n\n'.format(coord)

    except GeneratorExit:
        cv2.destroyAllWindows()
        cap.release()


def event_stream():
    channel = r.pubsub()
    channel.subscribe('devices')

    for msg in channel.listen():
        msg = msg['data'].decode('utf-8') if msg['data'] is not 1 else msg['data']
        yield 'data: {}\n\n'.format(msg)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/selector')
def selector():
    return Response(select(), mimetype='text/event-stream')


@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/video_capture')
def video_capture():
    return Response(track(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
