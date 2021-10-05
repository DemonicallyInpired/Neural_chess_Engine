#!/usr/bin/env python3
import numpy as np
import os 
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch import optim
from torch.utils.data import DataLoader

class ChessData(Dataset): 
    def __init__(self, directory, name):
        self.directory = os.path.join(os.getcwd(),directory)
        self.name = name
        data = np.load(os.path.join(self.directory, self.name), allow_pickle=True)
        self.seralized_state = data['seralized_state']
        self.game_results = data['game_result']
        print(f"lodaded {self.seralized_state.shape}{self.game_results.shape}")
    def __len__(self): 
        return self.seralized_state.shape[0]
    def __getitem__(self, idx): 
        return self.seralized_state[idx], self.game_results[idx]
class Network(nn.Module): 
    def __init__(self): 
        super(Network, self).__init__()
        self.h1 = nn.Conv2d(5, 16, kernel_size=3, padding=1)
        self.h2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
        self.h3 = nn.Conv2d(16, 32, kernel_size=3, stride=2)
        
        self.h11 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.h12 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.h13 = nn.Conv2d(32, 64, kernel_size=3, stride=2)
        
        self.h21 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.h22 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.h23 = nn.Conv2d(64, 128, kernel_size=2, stride=2)
        
        self.h31 = nn.Conv2d(128, 128, kernel_size=1)
        self.h32 = nn.Conv2d(128, 128, kernel_size=1)
        self.h33 = nn.Conv2d(128, 128, kernel_size=1)
        
        self.output = nn.Linear(128, 1)

    def forward(self, inp): 
        inp = F.relu(self.h1(inp))
        inp = F.relu(self.h2(inp))
        inp = F.relu(self.h3(inp))
        
        inp = F.relu(self.h11(inp))
        inp = F.relu(self.h12(inp))
        inp = F.relu(self.h13(inp))
        
        inp = F.relu(self.h21(inp))
        inp = F.relu(self.h22(inp))
        inp = F.relu(self.h23(inp))
        
        inp = F.relu(self.h31(inp))
        inp = F.relu(self.h32(inp))
        inp = F.relu(self.h33(inp))
        
        inp = inp.view(-1, 128)
        inp = self.output(inp)

        return F.tanh(inp)

if __name__ == "__main__":  
    try: 
        Directory = input('Enter the dataDir ')
        name = input('Enter the dataset filename ')
        device = input('Enter device')
        Data = ChessData(Directory, name)
    except Exception as e: 
        print(e)
        exit(0)
    train_loader = DataLoader(Data, batch_size = 256, shuffle=True)
    model = Network()
    optimizer = optim.Adam(model.parameters())
    mseloss = nn.MSELoss()
    if device == "cuda": 
        model.cuda()
    model.train()

    for epochs in range(100):
        all_loss = 0
        num_loss = 0
        epochs = 0
        for batch_idx, (data, target) in enumerate(train_loader): 
            target = target.unsqueeze(-1)
            data, target = data.to(device), target.to(device)
            data = data.float()
            target = target.float()

            optimizer.zero_grad()
            output = model(data)
            

            loss = mseloss(output, target)
            loss.backward()
            optimizer.step() 

            all_loss += loss.item()
            num_loss += 1

            print("%3d: %f"%(epochs, all_loss/num_loss))
            epochs += 1
            if((all_loss/num_loss) <= 0.01): 
                torch.save(model.state_dict(), str(os.getcwd() + "/model" + "/checkpoint.pth"))
                print("Model saved!")
                exit(0)
            