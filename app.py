import cv2
import json
import redis
from flask import Flask, Response, render_template
from zerotouch.tracking import FingerTracker, HandTracker
from zerotouch.motion import MotionOrder
from zerotouch.devices import Device


app = Flask(__name__)
r = redis.StrictRedis(host='192.168.1.108', port=6379)


def select():
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)

    padding = 80
    framecount_l = 0
    framecount_r = 0
    hover = False
    hitbox = 'hitbox_l'

    try:
        while True:
            _, frame = cap.read()
            _, coords = tracker.track(frame)

            h, w, _ = frame.shape
            hl = (0, (w // 2) - padding)
            hr = ((w // 2) + padding, w)

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


def track_finger():
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


def track_movement():
    # don't mind hardcoded moves list
    # it's just a demo after all
    moves = {
        'volume_up': [0, 1, 3, 2],
        'volume_down': [0, 2, 3, 1],
        'swipe_left': [0, 1],
        'swipe_right': [1, 0],
        'scroll_up': [2, 0],
        'scroll_down': [0, 2]
    }

    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    order = MotionOrder(moves=moves)
    areas_set = False

    try:
        while cap.isOpened():
            _, frame = cap.read()
            h, w, _ = frame.shape

            if not areas_set:
                order.set_capture_area(frame, n_areas=4, padding=20)
                areas_set = True

            frame, coords = tracker.track(frame)

            if len(coords) > 0:
                c = coords[0]
                # TODO remove drawing
                active = order.register(frame, c)
                payload = json.dumps({'active': active, 'move': None})

            else:
                move = order.parse()
                payload = json.dumps({'active': None, 'move': move})

            yield 'data: {}\n\n'.format(payload)

    except GeneratorExit:
        cv2.destroyAllWindows()
        cap.release()
        tracker.close_tf_session()


def device_datastream():
    channel = r.pubsub()
    channel.subscribe('devices')

    for msg in channel.listen():
        msg = msg['data'].decode('utf-8') if msg['data'] is not 1 else msg['data']
        yield 'data: {}\n\n'.format(msg)


@app.route('/')
def index():
    # TODO dev override
    # return render_template('index.html')
    return render_template('device_settings.html')


@app.route('/device_select')
def device_select():
    return render_template('device_select.html')


@app.route('/device_settings')
def device_settings():
    return render_template('device_settings.html')


@app.route('/selector')
def selector():
    return Response(select(), mimetype='text/event-stream')


@app.route('/device_datastream')
def stream():
    return Response(device_datastream(), mimetype='text/event-stream')


@app.route('/finger_tracking')
def video_capture():
    return Response(track_finger(), mimetype='text/event-stream')


@app.route('/motion_tracking')
def motion_tracking():
    return Response(track_movement(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
