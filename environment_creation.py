import numpy as np
import pydirectinput
import gymnasium as gym
from gymnasium import spaces
import time
import cv2
from mss import mss
import pytesseract
from stable_baselines3.common.env_checker import check_env
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class GoBattle(gym.Env):
    
    # metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self, render_mode=None, size=5):
        self.i = 0
        self.game_location = {'top': 210, 'left': 520, 'width': 900, 'height': 400}
        self.done_location = {'top': 230, 'left': 700, 'width': 280, 'height': 130}
        self.XP = {'top': 355, 'left': 930, 'width': 70, 'height': 45}
        self.anuncement = {'top': 315, 'left': 150, 'width': 140, 'height': 25}
        self.health = {'top': 235, 'left': 105, 'width': 40, 'height': 25}
        self.dimond = {'top': 222, 'left': 1697, 'width': 40, 'height': 40}
        self.disconnect = {'top': 355, 'left': 735, 'width': 440, 'height': 40}
        self.Epoc = 0
        # Observations are dictionaries with the agent's and the tar8get's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(low=0, high=255, shape=(1, 83, 100,) ,dtype=np.uint8)
        self.action_space = spaces.Discrete(7)
        self.window = None
        self.clock = None
        self.reward67 = 0
        self.reward = 0
        self.pun = False



    def reset(self, seed=None, options=None):
        
        # 
        pydirectinput.keyDown('8')
        pydirectinput.keyUp('8')
        time.sleep(9)
        pydirectinput.click(x=990, y=777)
        self.reward = self.reward67
        pydirectinput.keyDown('space')
        pydirectinput.keyUp('space')
        self.pun = False
        self.observation =  self.get_observation()
        self.info = {}
        
        self.reward = self.step
        
        return self.observation, self.info 
    def get_kill(self):
        with mss() as cap:
            a_cap = np.array(cap.grab(self.anuncement))
            img_bgr = cv2.cvtColor(np.array(a_cap), cv2.COLOR_BGR2GRAY)
            img_br = cv2.addWeighted(img_bgr, 1.5, 0, 0, 0)
            res = pytesseract.image_to_string(img_br)
            KILL_strings = ["You"]
            KILL=False
            if res[:3] in KILL_strings:
                KILL = True
            else:
                pass
            return res,KILL 


    def get_done(self):

        template = cv2.imread("skull.png")
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (h, w) = template.shape[:2]

        start_time = time.time()
        mon = {'top': 230, 'left': 700, 'width': 280, 'height': 130}
        with mss() as cap:
            while True:
                last_time = time.time()
                img = cap.grab(mon)
                img = np.array(img)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                meth = 'cv2.TM_CCOEFF'
                method = eval(meth) 
                result = cv2.matchTemplate(gray, template, method)
                (_, maxVal, _, _) = cv2.minMaxLoc(result)
                threshold = 4500000

                # Get the location of the matched area
                loc = np.where(maxVal >= threshold)

                # If a match is found
                
                if maxVal >= threshold:
                    if not self.pun:
                        self.reward67 = self.reward67-300
                        self.pun = True
                    else:
                        break
                    self.Epoc += 1
                    pydirectinput.keyDown('7')
                    pydirectinput.keyUp('7')
                    # time.sleep(3)
                    

                    pydirectinput.click(x=990, y=777)
                    pydirectinput.keyDown('space')
                    pydirectinput.keyUp('space')
                    
                else:
                    break
                break

    
    def step(self, action):
        pun = True
        self.reward67 = 0
        # img = np.array(mss().grab(self.disconnect))
        # img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        # img_br = cv2.addWeighted(img_bgr, 1.5, 0, 0, 0)
        # text = pytesseract.image_to_string(img_br)[:3]
        # if text == "You":
        #     pydirectinput.click(955,669)
        #     time.sleep(3)
        #     pydirectinput.click(1660,800)
        #     pydirectinput.click(1111,425)
       
        self.reward = 0
        action_map = {
            0:'space',
            1: 'v', 
            2: 'no_op',
            3: 'w',
            4: 'a',
            5: 's',
            6: 'd'
        }
        if action !=2:
            pydirectinput.press(action_map[action])
            
       


        self.get_done() 
        self.observation = self.get_observation()
        self.reward67 = self.reward67-50
        self.i += 1
        if self.i % 14 == 0:
            res ,kill = self.get_kill()
            if kill:
                self.reward67 +=100

                print(res)
            else:
                pass
        else:
            pass
        with mss() as cap:
            img = cap.grab(self.health)
            img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            img_br = cv2.addWeighted(img_bgr, 1.5, 0, 0, 0)
            hp = pytesseract.image_to_string(img_br, config="digits")
        
        self.info = {'hp':hp
            
        }
        self.terminated = False

        # print(f'reward [{self.reward}]')
        self.reward = self.reward67
        print(f'done reward [{self.reward}] Epsoid [{self.Epoc}] hp {hp}')

        return self.observation, self.reward, self.terminated, False, self.info
    def get_observation(self):
        with mss() as cap:
            raw = np.array(cap.grab(self.game_location))[:,:,:3].astype(np.uint8)
            gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (100,83))
            channel = np.reshape(resized, (1,83,100))
            return channel
    

env = GoBattle()
# It will check your custom environment and output additional warnings if needed
check_env(env)


