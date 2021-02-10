#!/usr/bin/env python3

import Skyconfig as game
from Skyconfig import log 
import numpy


# dumb agent, always pick up from discard
# place it in first open spot or higher card swap you come to, iterating
# never play the last card, instead just swap first card again

def playTurn( board ):
	
	card = game.discard
	
	for r in range(game.num_rows):
		for c in range(game.num_cols):
			if r==game.num_rows and c==game.num_cols:
				game.discard = board[0][0][0]
				board[0][0][0] = card
				
			if board[r][c][1]==0:
				game.discard = board[r][c][0]
				board[r][c][1] = 1
				board[r][c][0] = card
				return
			elif board[r][c][0]>card:
				game.discard = board[r][c][0]
				board[r][c][0] = card
				return
			