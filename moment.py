
from time import sleep
from win32dic import VK_CODE
import win32api , win32con , win32gui



class moment():
    def L_dash():
        self.KeyClick('w')
        self.KeyClick('a')
        self.KeyClick('a')

    def R_dash():
        self.KeyClick('w')
        self.KeyClick('d')
        self.KeyClick('d')
    def R_side():
        self.KeyClick('a')
        self.KeyClick('d')
        self.KeyClick('v')

    def L_side():
        self.KeyClick('d')
        self.KeyClick('a')
        self.KeyClick('v')

    def L_upper():
        self.KeyClick('s')
        self.KeyClick('d')
        self.KeyClick('v')
        self.time.sleep(0.8)

    def R_upper():
        self.KeyClick('s')
        self.KeyClick('a')
        self.KeyClick('v')
        self.time.sleep(0.8)

    def D_Attack():
        self.KeyClick('w')
        self.KeyClick('s')
        self.KeyClick('s')
        self.KeyClick('v')
        self.time.sleep(0.8)

    def KeyClick(key):
        try:
            win32api.keybd_event(VK_CODE[key], 0, 0, 0)
            time.sleep(0.1)  # You may need to adjust this delay based on your requirements
            win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
        except KeyError:
            print(f"Key {key} not found in VK_CODE dictionary.")

    def KeyHold(key):
        try:
            win32api.keybd_event(VK_CODE[key], 0, 0, 0)
            time.sleep(1)  # You may need to adjust this delay based on your requirements
            win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
        except KeyError:
            print(f"Key {key} not found in VK_CODE dictionary.")

