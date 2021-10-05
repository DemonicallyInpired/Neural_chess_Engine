#!/usr/bin/env python3
import os
import chess.pgn
import numpy as np
from state import State
def ReadPGN(path, no_of_sample = None):
    count = 0
    seralized_states, game_results = [], []  
    for fn in os.listdir(path): 
        while True: 
            try: 
                pgn = open(os.path.join(path,fn))
                game = chess.pgn.read_game(pgn)
            except Exception as e: 
                print(e)
                break
            
            result = game.headers["Result"]
            value = {"1/2-1/2": "0", "1-0": "1", "0-1": "-1"}[result]
            board = game.board()
            for i, move in enumerate(game.mainline_moves()): 
                board.push(move)
                #print(board, board.shredder_fen())
                #print(value, State(board).seralize()[:,:,0])
                ser = State(board).seralize()[:,:,0]
                seralized_states.append(ser)
                game_results.append(value)
                if(no_of_sample is not None and len(seralized_states) > no_of_sample): 
                    return seralized_states, game_results
            print("parsing game {} got {} examples".format(count, len(seralized_states)))
            count += 1
        #print(seralized_states, game_results)      
if __name__ == "__main__":  
    path = input('Enter the path ')
    N = int(input('Enter the no of samples to generate '))
    seralized_state, game_results = ReadPGN(path, N)
    np.savez("processed_data/data.npz", seralized_state = seralized_state, game_result = game_results)