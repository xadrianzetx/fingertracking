import cv2
import json
import redis
from flask import Flask, Response, render_template
from zerotouch import FingerTracker, HandTracker, Device


app = Flask(__name__)
r = redis.StrictRedis(host='192.168.1.108', port=6379)


def select():
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)

    framecount_l = 0
    framecount_r = 0
    hover = False
    hitbox = 'hitbox_l'

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
                    framecount_l += 1
                    hover = True
                    hitbox = 'hitbox_l'

                elif hr[0] < x < hr[1]:
                    framecount_r += 1
                    hover = True
                    hitbox = 'hitbox_r'

                else:
                    framecount_l = 0
                    framecount_r = 0
                    hover = False
                    hitbox = 'hitbox_l'

            data = {'fl': framecount_l, 'fr': framecount_r, 'hover': hover, 'hitbox': hitbox}
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


def device_datastream():
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


@app.route('/device_select')
def device_select():
    return render_template('device_select.html')


@app.route('/device_settings')
def device_settings():
    return render_template('device_settings.html')


@app.route('/device_datastream')
def stream():
    return Response(device_datastream(), mimetype='text/event-stream')


@app.route('/video_capture')
def video_capture():
    return Response(track(), mimetype='text/event-stream')


if __name__ == '__main__':
    # TODO fix confusing naming ffs
    app.debug = True
    app.run(threaded=True)
