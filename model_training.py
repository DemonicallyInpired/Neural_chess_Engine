#!/usr/bin/env python3
import numpy as np
import os 
from torch.utils.data import Dataset

class ChessData(Dataset): 
    def __init__(self, directory, name):
        self.directory = os.path.join(os.getcwd(),directory)
        self.name = name
        data = np.load(os.path.join(self.directory, self.name))
        self.seralized_state = data['seralized_state']
        self.game_results = data['game_result']
        print(f"lodaded {self.seralized_state.shape}{self.game_results.shape}")
    def __len__(self): 
        return self.seralized_state.shape[0]
    def __getitem__(self, idx): 
        return {"seralized_state": self.seralized_state[idx], "game_result": self.game_results[idx]}
if __name__ == "__main__": 
    Directory = input('Enter the dataDir ')
    name = input('Enter the dataset filename ')
    Data = ChessData(Directory, name)
