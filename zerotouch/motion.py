import cv2
import numpy as np


class CaptureArea:

    def __init__(self, area_id, coords, h, w, padding):
        self.id = area_id
        self._ay = coords[0]
        self._ax = coords[1]
        self._by = self._ay + h - padding
        self._bx = self._ax + w - padding

    def draw(self, frame, fill):
        cv2.rectangle(frame, (self._ax, self._ay), (self._bx, self._by), (255, 0, 0), fill, 1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(self.id), (self._ax, self._ay + 200), font, 4, (0, 0, 0), 2, cv2.LINE_AA)

    def is_active(self, coord):
        if self._ax < coord[0] < self._bx and self._ay < coord[1] < self._by:
            return True

        else:
            return False


class MotionOrder:

    def __init__(self, motions):
        self._areas = []
        self._order = []
        self._motions = motions

    def set_capture_area(self, frame, n_areas, padding):
        h, w, _ = frame.shape
        pad_h = h // (n_areas // 2)
        pad_w = w // (n_areas // 2)

        y_coords = [i * pad_h for i in range(n_areas // 2)]
        x_coords = [i * pad_w for i in range(n_areas // 2)]
        area_id = 0

        for y in y_coords:
            for x in x_coords:
                a = CaptureArea(area_id, (y, x), pad_h, pad_w, padding)
                self._areas.append(a)
                area_id += 1

    def register(self, frame, coord):
        for area in self._areas:
            if area.is_active(coord):
                area.draw(frame, -1)
                self._order.append(area.id)

            else:
                area.draw(frame, 2)

    def parse(self):
        if len(self._order) > 0:
            _, indices = np.unique(self._order, return_index=True)
            motion = [self._order[idx] for idx in sorted(indices)]
            print(motion)

        self._order.clear()
        # TODO compare motion to pre-defined gestures and output
