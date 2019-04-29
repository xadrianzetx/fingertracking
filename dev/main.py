import cv2
import redis
from fingertracking import FingerTracker, HandTracker, Device


def rescale_frame(frame, w=130, h=130):
    width = int(frame.shape[1] * w / 100)
    height = int(frame.shape[0] * h / 100)
    
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def main():
    # r = redis.StrictRedis(host='192.168.1.108', port=6379)
    capture = cv2.VideoCapture(0)
    tracker = HandTracker()

    while capture.isOpened():
        _, frame = capture.read()
        frame, coords = tracker.track(frame)

        h, w, _ = frame.shape
        a = (0, (w // 2) - 80)
        b = ((w // 2) + 80, w)

        if len(coords) > 0:
            coord = coords[0]
            print(a, coord)

            if a[0] < coord[0] < a[1]:
                cv2.rectangle(frame, (0, 0), ((w //2), h), (255, 0, 0), -1, 1)

            elif b[0] < coord[0] < b[1]:
                cv2.rectangle(frame, ((w // 2), 0), (w, h), (0, 0, 255), -1, 1)

            else:
                cv2.rectangle(frame, (0, 0), (w, h), (255, 0, 0), 2, 1)

        cv2.imshow('tracker', rescale_frame(frame))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    capture.release()


if __name__ == "__main__":
    main()
