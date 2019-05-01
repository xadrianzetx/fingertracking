import json


class Device:

    def __init__(self, name, connection):
        self._name = name
        self._con = connection
        self._hover = False
        self._active = False
        self._refresh = False
        self.ax = None
        self.bx = None
        self.frames = 0

    def _push(self):
        # prepare payload and push status
        payload = {'device': self._name, 'hover': self._hover, 'active': self._active}
        self._con.set(self._name, json.dumps(payload))
        self._con.publish('devices', json.dumps(payload))

    def set_hit_area(self, ax, bx):
        self.ax = ax
        self.bx = bx

    def hover(self):
        # count hover time
        self._hover = True
        self._refresh = True
        self.frames += 1
        self._push()

    def toggle(self):
        # zero out frames and switch on/off
        self.frames = 0
        self._refresh = True
        self._active = not self._active
        self._push()

    def inactive(self):
        # cursor out
        self.frames = 0

        if self._refresh:
            # limit db updates. push only if necessary
            self._hover = False
            self._refresh = False
            self._push()
