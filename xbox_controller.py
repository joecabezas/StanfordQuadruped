import threading
from inputs import get_gamepad

# modified from
# https://github.com/kevinhughes27/TensorKart/blob/master/utils.py
class XboxController(object):
    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def parseStick(self, value):
        return value / ((1<<15) - (1 if value>0 else 0))

    def parseTrigger(self, value):
        return value / ((1<<8) - 1)

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = self.parseStick(event.state)
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = self.parseStick(event.state)
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = self.parseStick(event.state)
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = self.parseStick(event.state)
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = self.parseTrigger(event.state)
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = self.parseTrigger(event.state)
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'ABS_HAT0X':
                    self.LeftDPad = 1 if event.state < 0 else 0
                    self.RightDPad = 1 if event.state > 0 else 0
                elif event.code == 'ABS_HAT0Y':
                    self.UpDPad = 1 if event.state < 0 else 0
                    self.DownDPad = 1 if event.state > 0 else 0

if __name__ == '__main__':
    import time
    gamepad = XboxController()
    while True:
        print(gamepad.RightBumper)
        time.sleep(0.05)
