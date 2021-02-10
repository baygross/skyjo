#!/usr/bin/env python3
import Skyconfig as game
from Skyconfig import log 
import numpy


def playTurn( board ):
	_chooseCard(board)


# Decide whether to pickup, or draw
def _chooseCard( board ):
	log("choosing card, current discard is ", game.discard)
	
	# if its a good card in discard pile, pick it up and play it
	if (game.discard <= 2) or (game.discard in _twoCols(board)):
		log("--> picked up discard")
		_playCard(board, game.discard)
		return
	
	# otherwise draw from deck
	drawncard = game.deck.pop()
	log("--> picked from deck, got", drawncard)
	
	# and play it if its a good card
	if (drawncard <= 3) or (drawncard in _twoCols(board)):
		_playCard(board, drawncard)
		return
	
	# or play it if its an okay card and late in game
	m = _maxDumbCard(board)
	if (cardsLeft(board) < 3 and drawncard < m[0]):
		_swapHighCard(board, drawncard)
		return
	
	# otherwise discard and flip
	game.discard = drawncard
	log("--> discarded and flipped")
	_flipNewCard(board)
	return

# returns maximum card not in a twofer set; and r/c index
def _maxDumbCard(board):
	
	log("max dumb card")
	# find a high card
	for n in (12, -2, -1):
		for r in board:
			for c in range(game.num_cols):
				if r[c][1] and r[c][0] == n: 
					
					# then see if it is in a straight
					other_col_cards = _visibleCol(board, c)
					other_col_cards.remove(n)
					if n in other_col_cards:
						next
						
					# otherwise return max card n and r, c indexes
					return [n, r, c]
	
def _swap_high_card(board, card):
	log("swapping high card!")
	n, r, c = _maxDumbCard(board)
	if c != card:
		log("oh no, max card function has an error")
		exit()
		
	game.discard = board[r][c][0]
	board[r][c][0] = card	




# Play a known good card. Only called with good cards
def _playCard(board, card):

	log("--> playing ", card)
	
	cols_to_consider = []
	
	# limit play to single column if we have a two-run already in that col	
	if card in _twoCols(board):
		for c in range(game.num_cols):
			visible_col_cards = _visibleCol(board, c)
			u, count = numpy.unique(visible_col_cards, return_counts=True)
			dup = (u[(count > 1)*(count < game.num_rows) ])
			if dup == card:
				log("appending col because 2 match")
				cols_to_consider.append(c)
				
	# otherwise choose a col that already has at least a one-run
	if len(cols_to_consider)==0:
		for c in range(game.num_cols):
			visible_col_cards = _visibleCol(board, c)
			if card in visible_col_cards:
				log("appending col because 1 match")
				cols_to_consider.append(c)

	# otherwise just add all cols
	if len(cols_to_consider)==0:
		cols_to_consider = range(game.num_cols)
			
	log("cols considered = ", cols_to_consider)
	
	# iterate through col or cols
	for c in cols_to_consider:
		# first get rid of any high cards
		for r in range(game.num_rows):
			if (board[r][c][1]==1 and board[r][c][0] >= 4 and board[r][c][0] != card):
				board[r][c][1] = 1
				game.discard = board[r][c][0]
				board[r][c][0] = card
				return

		# otherwise try first unflipped space
		for r in range(game.num_rows):		
			if board[r][c][1]==0:
				board[r][c][1] = 1
				game.discard = board[r][c][0]
				board[r][c][0] = card
				return
		
		# otherwise if only one col, do whatever cell remains (visible card, under 4, not part of straight)
		if len(cols_to_consider) == 1:
			for r in range(game.num_rows):		
				if board[r][c][0]!=card:
					game.discard = board[r][c][0]
					board[r][c][0] = card
					return
			

def _flipNewCard(board):
	for r in range(game.num_rows):
		for c in range (game.num_cols):
			if board[r][c][1]==0:
				board[r][c][1] = 1
				return


def _visibleCol(board, col):
	visible_col_cards = []
	for r in range(game.num_rows):
		if board[r][col][1]:
			visible_col_cards.append(board[r][col][0])
	return visible_col_cards		
			
# returns array of card numbers that currently exist in a 2-of-3 col 
def _twoCols( board ):	
	dup = []
	for c in range(game.num_cols):
		visible_col_cards = _visibleCol(board, c)
		u, count = numpy.unique(visible_col_cards, return_counts=True)
		dup.append(u[(count > 1)*(count < game.num_rows) ])
	return dup

# returns int of how many cards are left on a board. accepts board pointer as arg
def cardsLeft( board ):
	cardsLeft = 0; 
	for r in board:
		for c in r:
			cardsLeft +=1 if not(c[1]) else 0
	return cardsLeft