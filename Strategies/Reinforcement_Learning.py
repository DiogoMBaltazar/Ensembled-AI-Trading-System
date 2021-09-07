import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

# Gym stuff
import gym
import gym_anytrading
from gym_anytrading.envs import StocksEnv

# Stable baselines - rl stuff
from stable_baselines import A2C, PPO2, DDPG

from stable_baselines import SAC
from stable_baselines import TD3
from stable_baselines.common.vec_env import DummyVecEnv

# Processing libraries
import numpy as np
import pandas as pd
from Strategies.PCA import *
from Utilities.Graphs import *
from Utilities.config import *
from Utilities.util_funcs import *
from Utilities.Database_funcs import *
from Strategies.FeatureEngineering import *


# https://github.com/nicknochnack/Reinforcement-Learning-for-Trading/blob/main/Reinforcement%20Learning%20GME%20Trading%20Tutorial.ipynb

# This script will return the best performing agent based on SR among A2C, PPO, DDPG for a given rolling window


class ReinforcementLearning(object):

    def __init__(self):
        
        print("|--------------------------------------------------|")
        print("|Reinforcement Learning Engine has been initialized|")
        print("|--------------------------------------------------|")

        pass

    def add_signals(env):
        
        print(env.df.columns)            

        start = env.frame_bound[0] - env.window_size
        end = env.frame_bound[1]
        prices = env.df.loc[:, 'Close'].to_numpy()[start:end]
        signal_features = env.df.loc[:, env.df.columns != "Close"].to_numpy()[start:end]
        return prices, signal_features


    def rl_agents(self, data):
        
        # TODO // Ensemble PPO, DDPG & A2C agents
        # TODO // Get training/test data

        self.data = data

        self.data.drop(columns=["crypto_id"], inplace=True)

        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data.set_index('date', inplace=True)

        self.data = self.data.rename(columns={"close": "Close"})

        self.columns = self.data.columns

        # Gym set-up
        env = gym.make('stocks-v0', df=self.data, frame_bound=(15,30), window_size=15) 
        # window_size defines our lookback period
        
        # env.signal_features
        # env.action_space

        state = env.reset()

        while True: 
            action = env.action_space.sample()
            n_state, reward, done, info = env.step(action)
            if done: 
                print("info", info)
                break

        pass
    
        env2 = MyCustomEnv(df=self.data, window_size=15, frame_bound=(15,60))
    

        ## training event
        env_maker = lambda: env2
        env = DummyVecEnv([env_maker])

        ## testing event
        # env_maker = lambda: env2
        # env = DummyVecEnv([env_maker])

        modelA2C = A2C('MlpLstmPolicy', env, verbose=2) 
        modelA2C.learn(total_timesteps=5000) # adjust accordingly

        modelDDPG = DDPG('MlpLstmPolicy', env, verbose=2) 
        modelDDPG.learn(total_timesteps=5000) # adjust accordingly

        modelPPO2 = PPO2('MlpLstmPolicy', env, verbose=2) 
        modelPPO2.learn(total_timesteps=5000) # adjust accordingly

        env = MyCustomEnv(df=self.data, window_size=15, frame_bound=(15,90))
        obs = env.reset()
        
        while True: 
            obs = obs[np.newaxis, ...]
            action, _states = modelA2C.predict(obs)
            obs, rewards, done, info = env.step(action)
            if done:
                print("info", info)
                break

        Graphs.RL_agents(self, env)


class MyCustomEnv(StocksEnv):
    _process_data = ReinforcementLearning.add_signals