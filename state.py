#!/usr/bin/env python3
import chess
from chess.svg import piece
import numpy as np
class State(object): 
    count = 0
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
        board_state = np.zeros((64), np.uint8)
        for i in range(64): 
            pieces_at_p = self.board.piece_at(i)
            if pieces_at_p is not None: 
                board_state[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6, \
                "p": 9, "n": 10, "b": 11, "r": 12, "q": 13, "k": 14}[pieces_at_p.symbol()]
        if(self.board.has_queenside_castling_rights(chess.WHITE)): 
            assert(board_state[0] == 4)
            board_state[0] = 7
        if(self.board.has_kingside_castling_rights(chess.WHITE)): 
            assert(board_state[7] == 4)
            board_state[7] = 7
        if(self.board.has_queenside_castling_rights(chess.BLACK)): 
            assert(board_state[56] == 8+4)
            board_state[56] = 8+7
        if(self.board.has_kingside_castling_rights(chess.BLACK)):
            assert(board_state[63] == 8+4)
            board_state[63] = 8+7
        if(self.board.ep_square is not None): 
            assert(board_state[self.board.ep_square] == 0) 
            board_state[self.board.ep_square] = 8
        board_state = np.reshape(board_state, (8, 8))
        state = np.zeros((8, 8, 5))
        state[:,:,0] = (board_state >> 3)&1
        state[:,:,1] = (board_state >> 2)&1
        state[:,:,2] = (board_state >> 1)&1
        state[:,:,3] = (board_state >> 0)&1
        state[:,:,4] = (self.board.turn * 1.0)
        seralizer = self.board.shredder_fen()
        #print(state, seralizer)
        return state
if __name__ == "__main__": 
    s = State()
    s.seralize()
