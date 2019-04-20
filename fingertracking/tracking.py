import cv2
import numpy as np


class FingerTracker:

    def __init__(self):
        self._vertex_ax = None
        self._vertex_ay = None
        self._vertex_bx = None
        self._vertex_by = None
        self._histogram = None

    @staticmethod
    def _calculate_centroid(contour):
        m = cv2.moments(contour)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])

        return cx, cy

    def _masking(self, frame):
        # get skin color distribution from sample
        blur = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0, 1], self._histogram, [0, 180, 0, 256], 1)
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))

        cv2.filter2D(dst, -1, disc, dst)

        # img thresholding and masking non skin tonned areas
        _, thresh = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh = cv2.merge((thresh, thresh, thresh))
        mask = np.bitwise_and(frame, thresh)

        # calculating hand contour coordinates
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, gray_thresh = cv2.threshold(gray, 0, 255, 0)
        contour, _ = cv2.findContours(gray_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contour

    def histogram(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        roi = hsv_frame[self._vertex_ay:self._vertex_by, self._vertex_ax:self._vertex_bx]

        self._histogram = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(self._histogram, self._histogram, 0, 255, cv2.NORM_MINMAX)

    def draw_sampling_area(self, frame):
        width, height, _ = frame.shape

        self._vertex_ax = int(11 * width / 20)
        self._vertex_ay = int(7 * height / 20)
        self._vertex_bx = int(self._vertex_ax + 50)
        self._vertex_by = int(self._vertex_ay + 50)

        return frame

    def track(self, frame, devices):
        contours = self._masking(frame)

        # get main contour
        areas = [cv2.contourArea(c) for c in contours]
        max_area = np.argmax(areas)
        contour = contours[max_area]

        # get centroid coordinates
        cx, cy = self._calculate_centroid(contour)
        tx, ty = contour[contour[:, :, 1].argmin()][0]

        # extrapolate to upper edge of frame
        z = np.polyfit([cx, tx], [cy, ty], 1)
        px = (0 - z[1]) / z[0]

        # draw hit areas
        width, height, _ = frame.shape
        h_ax = [x * width // 20 for x in [5, 10, 15]]
        h_bx = [x + 60 for x in h_ax]

        for device, ax, bx in zip(devices, h_ax, h_bx):
            device.set_hit_area(ax, bx)

        # update device status
        for device in devices:
            if device.bx > px > device.ax:
                if device.frames > 10:
                    device.toggle()

                else:
                    device.hover()

            else:
                device.inactive()

        return frame, px
