## Description: 
Neural_Chess is a Zero knowledege-based chess engine that uses a simple 1 look ahead neural network value function which takes in a serialized board and outputs a range from -1 to 1, where -1 means black is win, 1 means white is win.

## Defination of the value Network: 
V = f(states of the move)
Where V can assume the value as follows: 
-1: White Wins Board State
0: Draw Board State
1: Black Wins Board State

