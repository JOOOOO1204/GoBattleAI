from environment_creation import GoBattle
# Import os for file path management
import os 
# Import Base Callback for saving modelsdddddddddddddd
from stable_baselines3.common import env_checker
import tensorboard
# from stable_baselines3.common.envs import DummyVecEnv
# Import Frame Stacker Wrapper and GrayScaling Wrapper
from gymnasium.wrappers import GrayScaleObservation
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import PPO , DQN , A2C
# from gymnasium.wrappers import SubprocVecEnv
from stable_baselines3.common.vec_env import SubprocVecEnv, VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.policies import ActorCriticPolicy 
import time
# from torch import cpu
from stable_baselines3.common.logger import configure 
env = GoBattle()
# env = SubprocVecEnv([lambda: GoBattle()])
# env = Monitor(env=env)
# ewcsw3. Grayscale
# env = GrayScaleObservation(env, keep_dim=True)
# 4. Wrap inside the Dummy Environment
# env = SubprocVecEnv([lambda: env])
# 5. Stack the frames
# env = VecFrameStack(env, 5, channels_order='last')w


CHECKPOINT_DIR = './trainPPO_/'
LOG_DIR = './logsPPO_/'
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
# 
# This is the AI model started

# PPO model maker
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=LOG_DIR)

# DQN modelaswas
# model = DQN('CnnPolicy', env, tensorboard_log=LvOG_DIR, verbose=1, buffer_size=1000, learning_starts=100,)

# model = model.load('trainPPO_/150000.zip', print_system_info=True)

# obs = env.reset()
# while True: 
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)





try:
    model.learn(total_timesteps=99999999, callback=callback)
except KeyboardInterrupt:
    save_resa = input(print('do u want to save (n)'))
    if save_resa == 'n':
        
        # saves the model When there is a keyboard Intrrupt
        model.save(os.path.join(CHECKPOINT_DIR, 'resat_modle'))
        print('stopped with saving')
    else:
        print("stoped with out saving")




