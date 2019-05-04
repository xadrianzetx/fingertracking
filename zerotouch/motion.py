import numpy as np


class CaptureArea:

    def __init__(self, area_id, coords, h, w, padding):
        self.id = area_id
        self._ay = coords[0]
        self._ax = coords[1]
        self._by = self._ay + h - padding
        self._bx = self._ax + w - padding

    def is_active(self, coord):
        if self._ax < coord[0] < self._bx and self._ay < coord[1] < self._by:
            return True

        else:
            return False


class MotionOrder:

    def __init__(self, moves):
        self._areas = []
        self._order = []
        self._moves = moves

    def set_capture_area(self, frame, n_areas, padding):
        h, w, _ = frame.shape
        pad_h = h // (n_areas // 2)
        pad_w = w // (n_areas // 2)

        # evenly spread capture areas
        y_coords = [i * pad_h for i in range(n_areas // 2)]
        x_coords = [i * pad_w for i in range(n_areas // 2)]
        area_id = 0

        for y in y_coords:
            for x in x_coords:
                # init all areas
                a = CaptureArea(area_id, (y, x), pad_h, pad_w, padding)
                self._areas.append(a)
                area_id += 1

    def register(self, coord):
        for area in self._areas:
            if area.is_active(coord):
                self._order.append(area.id)

        return self._order

    def parse(self):
        k = None

        if len(self._order) > 0:
            # get unique areas visited, maintain visit order
            _, indices = np.unique(self._order, return_index=True)
            move = [self._order[idx] for idx in sorted(indices)]
            self._order.clear()

            for key in self._moves.keys():
                # match visit order to list of moves
                if self._moves[key] == move:
                    k = key

        return k
