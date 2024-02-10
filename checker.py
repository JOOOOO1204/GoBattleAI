from stable_baselines3.common.env_checker import check_env
import os

from environment_creation import GoBattle



env = GoBattle()
# It will check your custom environment and output additional warnings if needed
check_env(env)
       