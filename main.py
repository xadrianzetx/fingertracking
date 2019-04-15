import cv2
from handtracking.tracking import HandTracker


def rescale_frame(frame, w=130, h=130):
    width = int(frame.shape[1] * w / 100)
    height = int(frame.shape[0] * h / 100)
    
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def main():
    capture = cv2.VideoCapture(0)
    tracker = HandTracker()

    while capture.isOpened():
        _, frame = capture.read()

        frame = tracker.draw_sampling_area(frame)
        tracker.histogram(frame)
        frame, _ = tracker.track(frame)

        cv2.imshow('tracker', rescale_frame(frame))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    capture.release()


if __name__ == "__main__":
    main()
