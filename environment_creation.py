import numpy as np
import pydirectinput
import gymnasium as gym
from gymnasium import spaces
import time
import cv2
from mss import mss
import pytesseract
from time import sleep
from win32dic import VK_CODE
import win32api , win32con , win32gui 
# Corrected import statement
import pyautogui
# import ImageGrab

import pydirectinput
from stable_baselines3.common.env_checker import check_env
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class GoBattle(gym.Env):
    
    # metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self, render_mode=None, size=5):
        self.state = 0
        self.time_elapsed = 0
        self.max_time = 10  # Time in minutes before each step
        self.i = 0
        self.game_location = {'top': 400, 'left': 250, 'width': 110, 'height': 500}
        self.anuncement = {'top': 180, 'left': 170, 'width': 440, 'height': 45}
        self.health = {'top': 235, 'left': 105, 'width': 40, 'height': 25}
        self.Epoc = 0
        # Observations are dictionaries with the agent's and the tar8get's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(low=0, high=255, shape=(1,100,200,) ,dtype=np.uint8)
        self.action_space = spaces.Discrete(9)
        self.window = None
        self.clock = None
        self.reward = 0
        self.pun = False
        self.terminated = False
        self.done = False


    def reset(self, seed=None, options=None):
        # Reset the environment to its initial state
        self.state = 0
        self.i = 0
        self.time_elapsed = 0
        self.Epoc += 1
        print("resat")
        window_title = "GoBattle.io ⚔️ Battle to be the King! 👑 Play for free the best 2D MMO game - Brave"
        hwnd = win32gui.FindWindow(None, window_title)

        if hwnd != 0:
            # If the window is found, bring it to the foreground
            sleep(0.1)
            win32gui.SetForegroundWindow(hwnd)
        else:
            # Handle the case where the window is not found
            print(f"Window with title '{window_title}' not found.")

        # win32gui.SetForegroundWindow("GoBattle.io ⚔️ Battle to be the King! 👑 Play for free the best 2D MMO game - Brave")


       # pydirectinput.keyDown('space')
      #  pydirectinput.keyUp('space')
        self.pun = False
        self.observation =  self.get_observation()
        self.info = {
            # 'wepone' : 'string'
            }
        
        
        return self.observation, self.info 
    def get_kill(self):
        with mss() as cap:
            a_cap = np.array(cap.grab(self.anuncement))
            img_bgr = cv2.cvtColor(np.array(a_cap), cv2.COLOR_BGR2GRAY)
            img_br = cv2.addWeighted(img_bgr, 2, 0, 0, 0)
            res = pytesseract.image_to_string(img_br)
            KILL_strings = ["You"]
            KILL=False
            if res[:3] in KILL_strings:
                KILL = True
                print(res[:3])
                print(res)
            else:
                pass
            return res,KILL 


    def get_done(self):
        # px = ImageGrab.grab().load()
        x,y =  960, 920
        hdc = win32gui.GetDC(0)
        color = win32gui.GetPixel(hdc, x, y)
        win32gui.ReleaseDC(0, hdc)
        color_tuple = (color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF)
        if color_tuple[0] > 200 and color_tuple[1] > 200 and color_tuple[2] > 200:
            self.KeyClick('spacebar')
            done = True
            return done



       
    
    def step(self, action):
         # k = self.get_kill()
        # if k:
        #     self.reward67 += 100
        # pun = True
        self.reward = 0
        self.observation = self.get_observation()
        action_map = {
            0:'spacebar',
            1: 'v', 
            2: 'no_op',
            3: 'w',
            4: 'a',
            5: 's',
            6: 'd',
            7: 'c',
            8: 'e'
        }
        if action !=2:
            a = action_map[action]
            self.KeyClick(a)
            
       


        done = self.get_done()
        if done:

            self.reward -= 50
            self.reset()     
        
        self.i += 1
        if self.i % 7 == 0:
            res ,kill = self.get_kill()
            if kill:
                self.reward += 25

                print(res)

        # with mss() as cap:
            # img = cap.grab(self.health)
            # img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            # img_br = cv2.addWeighted(img_bgr, 1.5, 0, 0, 0)
            # hp = pytesseract.image_to_string(img_br, config="digits")

        self.info = {
            # wepone : 'string'
            # 'hp':hp
            
        }
        

        # print(f'reward [{self.reward}]')
        
        print(f'done reward [{self.reward}] Epsoid [{self.Epoc}] hp')
        return self.observation, self.reward, self.terminated, False, self.info 
    def get_observation(self):
            with mss() as sct:
                raw = np.array(sct.grab(self.game_location))[:,:,:3].astype(np.uint8)
                gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (200,100))
                channel = np.reshape(resized, (1,100,200))
                return channel
    def KeyClick(self,key):
        try:
            win32api.keybd_event(VK_CODE[key], 0, 0, 0)
            time.sleep(0.1)  # You may need to adjust this delay based on your requirements
            win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
        except KeyError:
            print(f"Key {key} not found in VK_CODE dictionary.")
    def find_all_windows(name):
        result = []
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
                result.append(hwnd)
            win32gui.EnumWindows(winEnumHandler, None)
            return result


    def KeyHold(key):
        try:
            win32api.keybd_event(VK_CODE[key], 0, 0, 0)
            time.sleep(1)  # You may need to adjust this delay based on your requirements
            win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
        except KeyError:
            print(f"Key {key} not found in VK_CODE dictionary.")

env = GoBattle()
# It will check your custom environment and output additional warnings if needed
check_env(env)


