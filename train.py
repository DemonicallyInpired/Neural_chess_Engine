#!/usr/bin/env python3
import os
import chess.pgn
from state import State
def ReadPGN(path): 
    count = 0
    for fn in os.listdir(path): 
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
            print(value, State(board).seralize())        
if __name__ == "__main__": 
    path = input('Enter the path ')
    ReadPGN(path)
