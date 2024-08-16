import  win32api , win32con
from win32dic import VK_CODE
import time


def KeyHoldDown(key):
    try:
        win32api.keybd_event(VK_CODE[key], 0, 0, 0)
    except KeyError:
        print(f"Key {key} not found in VK_CODE dictionary.")


def KeyHoldUpp(key):
    try:
        win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
    except KeyError:
        print(f"Key {key} not found in VK_CODE dictionary.")

if __name__ == "__main__":
    time.sleep(3)
    KeyHoldDown("a")
    time.sleep(9)
    KeyHoldUpp("a")

