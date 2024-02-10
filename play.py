from environment_creation import GoBattle
from stable_baselines3 import PPO
import time
CHECKPOINT_DIR = './ML/GOO/train88h/'8
LOG_DIR = './ML/GOO/logs88h/'
env = GoBattle()
model = PPO('CnnPolicy',env=env ,tensorboard_log=LOG_DIR)
model.load('ML/GOO/train88h/best_model_21000.zip')
for episode in range(5): 
    obs = env.reset()
    done = False
    total_reward = 0
    while not done: 
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(int(action))
        time.sleep(0.01)
        total_reward += reward
    print('Total Reward for episode {} is {}'.format(episode, total_reward))
    time.sleep(2)








