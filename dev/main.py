import cv2
import json
import redis
from zerotouch import FingerTracker, HandTracker, Device
from zerotouch.motion import MotionOrder


def rescale_frame(frame, w=130, h=130):
    width = int(frame.shape[1] * w / 100)
    height = int(frame.shape[0] * h / 100)
    
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def main():
    # r = redis.StrictRedis(host='192.168.1.108', port=6379)
    moves = {
        'volume_up': [0, 1, 3, 2],
        'volume_down': [0, 2, 3, 1],
        'swipe_left': [0, 1],
        'swipe_right': [1, 0],
        'scroll_up': [2, 0],
        'scroll_down': [0, 2]
    }

    capture = cv2.VideoCapture(0)
    tracker = HandTracker()
    order = MotionOrder(moves=moves)
    areas_set = False

    while capture.isOpened():
        _, frame = capture.read()
        h, w, _ = frame.shape

        if not areas_set:
            order.set_capture_area(frame, 4, 20)
            areas_set = True

        frame, coords = tracker.track(frame)

        if len(coords) > 0:
            c = coords[0]
            active = order.register(frame, c)
            payload = json.dumps({'active': active, 'move': None})

        else:
            move = order.parse()
            payload = json.dumps({'active': None, 'move': move})

        cv2.imshow('tracker', rescale_frame(frame))
        print(payload)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    capture.release()


if __name__ == "__main__":
    main()
