#!/usr/bin/env python3
import random
import numpy
import Skyconfig as game
import Skybay
import Skydumb

# Print all boards
def print_boards(fog_of_war = False):
	for p in range(game.num_players):
		print("Player "+str(p))
		print('\n'.join(
			['\t'.join(
				[str(cell[0]) if (cell[1] or fog_of_war) else "X" for cell in row]
			) for row in game.boards[p] ]
		))
		
# returns int of how many cards are left on a board. accepts board pointer as arg
def cardsLeft( board ):
	cardsLeft = 0; 
	for r in board:
		for c in r:
			cardsLeft +=1 if not(c[1]) else 0
	return cardsLeft

def boardTotal( board ):
	total = 0; 
	for r in board:
		for c in r:
			total += c[0]
	return total
	
	
def main():
	
	game.init()
	
	# Initiate deck
	for i in range(-2, 12):
		for j in range(10):
			game.deck.append(i)
	random.shuffle(game.deck)
	
	
	# Initiate boards
	for bid in range(game.num_players):
		game.boards.append([])
		for rid in range(game.num_rows):
			game.boards[bid].append([])
			for cid in range(game.num_cols):
				game.boards[bid][rid].append( [game.deck.pop(), 0] )
	
	# Flip first two cards
	for bid in range(game.num_players):
		game.boards[bid][0][game.num_cols-1][1]=1
		game.boards[bid][0][game.num_cols-2][1]=1
	
	# Initiate discard pile
	game.discard = game.deck.pop()
	
	#print_boards()
	#print_boards(True)
	
	bays_board = game.boards[0]
	opponents_board = game.boards[1]
	print_boards()
	
	while ( cardsLeft(bays_board) > 0 and cardsLeft(opponents_board) > 0 ):
		Skybay.playTurn(bays_board)
		Skydumb.playTurn(opponents_board)
		print_boards()
		
	# show final boards
	print_boards(True)
	
	print("\n---\nFinal Score:\n")
	print("Bay: ", boardTotal(bays_board))
	print("Opponent: ", boardTotal(opponents_board))
	
	

main()