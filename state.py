#!/usr/bin/env python3
import chess
import numpy as np
class State(object): 
    def __init__(self, board = None): 
        if(board == None): 
            self.board = chess.Board()
        else: 
            self.board = board
    def edges(self): 
        return(list(self.board.legal_moves))
    def value(self): 
        return 1
    def seralize(self): 
        assert(self.board.is_valid())
        board_state = np.zeros((8, 8), np.uint8)
        for i in range(64): 
            pieces_at_p = self.board.piece_at(i)
            if(pieces_at_p): 
                print(pieces_at_p, i)
                pass
        state = np.zeros((8, 8, 5))
        state[:,:,0] = (board_state >> 3)&1
        state[:,:,1] = (board_state >> 2)&1
        state[:,:,2] = (board_state >> 1)&1
        state[:,:,3] = (board_state >> 0)&1
        state[:,:,4] = (self.board.turn * 1.0)
        seralizer = self.board.shredder_fen()
        print(state)
        return seralizer
if __name__ == "__main__": 
    s = State()
    s.seralize()
