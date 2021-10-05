#!/usr/bin/env python3
import sys
import torch 
from state import State
from model_training import Network
import os

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

class Evaluate(object):
    def __init__(self): 
        self.path = input('Enter the model_name')
        self.model = Network()
    def load_model(self): 
        self.model.load_state_dict(torch.load(os.path.join(os.getcwd(), "model",self.path)))
        return self.model
    def __call__(self, sb): 
        self.model = self.load_model()
        sb = sb.seralize()[None]
        output = self.model(torch.tensor(sb).float())
        return float(output[0][0])

if __name__ == "__main__": 
    predict = Evaluate()
    sb = State()
    print(predict(sb))

    