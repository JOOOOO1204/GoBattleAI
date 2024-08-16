
#importing all the liberre

import numpy as np
import dxcam
import gymnasium as gym
import win32api , win32con , win32gui 
import time
import cv2
import pytesseract
from time import sleep
from win32dic import VK_CODE
from mss import mss
from stable_baselines3.common.env_checker import check_env
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'




class GoBattle(gym.Env):
    
    # metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self):
        
        # defing all the varables
        
        # self.state = 0
        # self.time_elapsed = 0
        # self.max_time = 10  # Time in minutes before each step
        # self.i = 0
        self.game_location = (250,  400, 500,  1110)
        self.anuncement = {'top': 180, 'left': 170, 'width': 440, 'height': 45}
        self.health = {'top': 235, 'left': 105, 'width': 40, 'height': 25}
        # self.Eposode = 0
        # Observations are dictionaries with the agent's and the tar8get's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(1,169,300,) ,dtype=np.uint8)
        # self.action_space = MultiDiscrete([8,8,8,8])
        
        self.action_space = gym.spaces.Discrete(7)
        # self.window = None
        # self.clock = None
        # self.reward = 0
        # self.pun = False
        # self.terminated = False
        # self.done = False
        # self.kills = 0
        # self.death = 0
        self.camera = dxcam.create(output_idx=0, device_idx=0 ,output_color="GRAY")


















    def reset(self, seed=None, options=None):
        # Reset the environment to its initial state
        
        # resating varables
        self.i = 0
        self.time_elapsed = 0
        # self.pun = False
        
        
        print(f'done reward [{self.reward}]')
        
        try:
            self.camera.stop()
        except:
            pass

        self.camera.start(target_fps=60)
        
        # bring the window front
        window_title = "GoBattle.io ⚔️ Battle to be the King! 👑 Play for free the best 2D MMO game - Brave"
        hwnd = win32gui.FindWindow(None, window_title)

        if hwnd != 0:
            # If the window is found, bring it to the foreground
            sleep(0.1)
            win32gui.SetForegroundWindow(hwnd)
        else:
            # Handle the case where the window is not found
            print(f"Window with title '{window_title}' not found.")

        
        
        # defining the return varable
        self.observation =  self.get_observation()
        self.info = {}
        
        
        return self.observation, self.info 
    




















    def step(self, key):
        Moment_keys = ['a', 'd', 's']
        key_states = {key: False for key in Moment_keys}
        # self.reward = 0
        # k = self.get_kill()
        # if k:
        #     self.reward += 100
        self.observation = self.get_observation()
        action_map = {
            0: 'no_op',
            1: 'w',
            2: 'a',
            3: 's',
            4: 'd',
            5:'spacebar',
            6: 'v', 
            
        }


        if key !=0:
            action = action_map[key]
            # self.KeyClick(action)
            

            # if soward is used check for kill

            if action == 'v':
                self.KeyClick(action)
                player_name ,kill = self.get_kill()

                if kill:
                    self.reward = 50
                    self.kills += 1
                    print(player_name)
            
            
            # `Moment_keys` contains the keys that trigger momentary actions.
            Moment_keys = ['a', 'd', 's']

            # `key_states` is a dictionary that stores the current state (pressed/released) of each key in `Moment_keys`.
            key_states = {key: False for key in Moment_keys}

            # `action` represents the key pressed by the user.
            # It is assumed that `action_map` is defined elsewhere in the code.
            action = action_map[key]

            # If the pressed key triggers a momentary action:
            if action in Moment_keys:
                # Toggle the state of the key.
                key_states[action] = not key_states[action]
                
                # If the key is pressed:
                if key_states[action]:
                    # Call a method to hold the key down.
                    self.KeyHoldDown(action)
                else:
                    # If the key is released:
                    # Call a method to release the key.
                    self.KeyHoldUp(action)
            # If the pressed key does not trigger a momentary action:
            else:
                # Call a method to simulate a click on the key.
                self.KeyClick(action)
                
            
       

        # checking if u died 
        # if yes calls reset() funtion
        done = self.get_done()
        if done:
            self.death += 1

            self.reward = -100
            self.reset()
            
        else:
            self.reward += 0.1
   

        
        
        # defining the return varable
        self.info = {}
        return self.observation, self.reward, self.terminated, False, self.info
    



























    def get_kill(self):
        with mss() as cap:
            a_cap = np.array(cap.grab(self.anuncement))
            img_bgr = cv2.cvtColor(np.array(a_cap), cv2.COLOR_BGR2GRAY)
            img_br = cv2.addWeighted(img_bgr, 2, 0, 0, 0)
            player_name = pytesseract.image_to_string(img_br)
            KILL_strings = ["You"]
            KILL=False
            if player_name[:3] in KILL_strings:
                KILL = True
                print(f'{player_name} died')
            else:
                print("no kill")
                pass
            return player_name,KILL 


    def get_done(self):
        # px = ImageGrab.grab().load()
        # x,y =  960, 920
        x,y = 669,850
        hdc = win32gui.GetDC(0)
        color = win32gui.GetPixel(hdc, x, y)
        win32gui.ReleaseDC(0, hdc)
        color_tuple = (color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF)
        if color_tuple[0] > 200 and color_tuple[1] > 200 and color_tuple[2] > 200:
            self.KeyClick('spacebar')
            self.camera.stop()
            done = True
            return done
 
    def get_observation(self):
                
                raw = np.array(self.camera.get_latest_frame()).astype(np.uint8)
                # gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(raw, (300,169))
                channel = np.reshape(resized, (1,169,300))
                
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
            
            
    def KeyHoldDown(_,key_key):
        try:
            win32api.keybd_event(VK_CODE[key_key], 0, 0, 0)
        except KeyError:
            pass
            print(f"Key {key_key} not found in VK_CODE dictionary.")


    def KeyHoldUpp(_ , key_key):
        try:
            win32api.keybd_event(VK_CODE[key_key], 0, win32con.KEYEVENTF_KEYUP, 0)
            
        except KeyError:
            pass
            print(f"Key {key_key} not found in VK_CODE dictionary.")


