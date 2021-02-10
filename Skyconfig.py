#!/usr/bin/env python3

def init():
	#
	# Globals
	global deck
	deck = []  		# the card deck. 10 of each card [-2..12]
	
	global boards
	boards = []     # array of player boards. all card values
	
	global discard
	discard = None
	
	#
	# Settings
	global num_rows
	num_rows = 3
	
	global num_cols
	num_cols = 4
	
	global num_players
	num_players = 2
	
	
def log(*args):
	print(*args)
	return