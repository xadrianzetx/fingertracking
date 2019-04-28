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
        frame, _ = tracker.track(frame)
        cv2.imshow('tracker', rescale_frame(frame))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    capture.release()


if __name__ == "__main__":
    main()
