from environment_creation import GoBattle
# Import os for file path management
import os 
# Import Base Callback for saving modelsdddddddddddddd
from stable_baselines3.common import env_checker
import tensorboard
# from stable_baselines3.common.envs import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
import time
from stable_baselines3.common.logger import configure 
env = GoBattle()
CHECKPOINT_DIR = './train021/'
LOG_DIR = './logs021/'
new_logger = configure(LOG_DIR, ["stdout", "csv", "tensorboard"])


class TrainAndLoggingCallback(BaseCallback):


    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path


    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, '{}'.format(+self.n_calls))
            self.model.save(model_path)

        return True


callback = TrainAndLoggingCallback(check_freq=1000, save_path=CHECKPOINT_DIR)
# model = DQN('CnnPolicy', env, tensorboard_log=LOG_DIR, verbose=1, buffer_size=1000, learning_starts=100,)
# model = PPO(policy="MlpPolicy", env=env, verbose=1)
model = PPO('CnnPolicy',env=env ,verbose=1 , ent_coef= 0.001)
model.set_logger(new_logger)
# model.learn(100000000000000000)s
#model = PPO.load('train01/15600.zip')

model.learn(total_timesteps=int(1e15), callback=callback)

# model.learn(total_timesteps=int(1e5), callback=callback)

for episode in range(5): 
    obs = env.reset()
    done = False
    total_reward = 0
    while not done: 
        action = model.predict(obs)
        obs, reward, done, info = env.step(int(action))
        time.sleep(0.01)
        total_reward += reward
    print('Total Reward for episode {} is {}'.format(episode, total_reward))
    time.sleep(2)


