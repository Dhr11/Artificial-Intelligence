#!/usr/bin/env python3
# nrooks.py : Solve the N-Rooks problem!
# Creator: David crandall(instructor) - gave the base problem, Dhruuv Agarwal rest :) 
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
# Similarly Nqueens problem, to place N queens on the board
#----------------------------------------------------------------------------------

# Updated and Written by Dhruuv Agarwal
# Worked on the basic template of Nrooks given by instructor, and extended
# it. Now it works for Nrooks and Nqueens with option to provide invalid states.

# The code is using DFS with condtions to help limit the successor state and thus 
# help us get a complete solution. The conditions and logic implemented for Nrooks
# and queens differ, hence they both have different successor functions defined. 


import sys
import collections
import time
import math
import re
# Count # of pieces in given row
Pieces = 0
pieces_row= []

def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board, Probtype, listofpoints):
	if re.match(Probtype,"nrook"):	Letter = "R"
	elif re.match(Probtype,"nqueen"):	Letter = "Q"
	else: Letter = "K"
	
	return "\n".join([ " ".join([ Letter if board[row][col] else "X" if (row,col) in listofpoints else "_" for col in range(0,N)]) for row in range(0,N)])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
	
	return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Function implemented to cross check entries in diagnol elements for Nqueens problem
# Implemented on basis of property observed in indices of a matrix
def diagnol_bookkeeping(board,r,c,leftD,rightD,colempty):
	leftD[r-c] = 1
	rightD[r+c] = 1
	
	if(c>=colempty[0]) :
		colempty[0]= c+1

colmax = 0	
# Get list of successors of given board state

	
def successorsRooks(board,listofpoints):

	temp=[]
	global colmax
	c= colmax
	[ temp.append(add_piece(board, r, c)) for r in range(0, N) if board[r][c] is 0 and count_pieces(board)<N and count_on_row(board, r) < 1 and count_on_col(board, c) < 1 and not temp and (r,c) not in listofpoints]
	c = c+1
	colmax= c
	return temp

def successorsQueens(board,listofpoints):
	leftD = {}
	rightD = {}
	colempty=[0]
		
	[diagnol_bookkeeping(board,r,c,leftD,rightD,colempty) for r in range(0,N) for c in range(0,N) if board[r][c] is 1]
	temp=[]
	
	c = colempty[0] 
	[ temp.append(add_piece(board, r, c)) for r in range(0, N) if board[r][c] is 0 and count_pieces(board)<N and count_on_row(board, r) < 1 and count_on_col(board, c) < 1 and (r-c) not in leftD and (r+c) not in rightD and (r,c) not in listofpoints]# and not temp ]
		
	return temp	

	# logic for knights to eliminate successor states
def knightneighbour(board):
	indicessum = set()
	
	for r in range(0, N):
		for c in range(0,N): 
			if board[r][c]:
				if (r+c-1)>=0:	indicessum.add(r+c-1) 
				if (r+c+1)<=2*N:	indicessum.add(r+c+1) 
				if (r+c-3)>=0:	indicessum.add(r+c-3) 	
				if (r+c+3)<=2*N:	indicessum.add(r+c+3)
	return indicessum				
# successor for nknights	
def successorsKnights(board,listofpoints):
	listnot = knightneighbour(board)
	temp=[]
	[ temp.append(add_piece(board, r, c)) for c in range(0,N) for r in range(0, N) if board[r][c] is 0 and count_pieces(board)<N and (r,c) not in listofpoints and r+c not in listnot]
	
	
	return temp		
# check if board is a goal state
def is_goal(board):

	return all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board,listofpoints, Probtype):
	fringe=[(initial_board)]
	
	i=1
	while len(fringe) > 0:
		successors = []
		if re.match(Probtype,"nqueen") :	successors = successorsQueens(fringe.pop(),listofpoints)
		elif re.match(Probtype,"nrook") :	successors = successorsRooks(fringe.pop(),listofpoints)
		elif re.match(Probtype,"nknight") :	successors = successorsKnights(fringe.pop(),listofpoints)
		for s in successors:
			if count_pieces(s) == N:
				if is_goal(s):
					return(s)
			fringe.append(s)
		i+=1		
	return False

# This is N, the size of the board. It is passed through command line arguments.
Probtype = str(sys.argv[1])
N = int(sys.argv[2])
P = int(sys.argv[3])
try:
	listofpoints = [(int(sys.argv[3+r+1])-1,int(sys.argv[3+r+2])-1) for r in range(0,2*P,2)]
except (RuntimeError):
	print("Input problem")
	
# The board is stored as a list-of-lists. Each inner list is a row of the board.

initial_board = [[0]*N]*N
solution = []
if Probtype in ["nrook","nqueen","nknight"]:
	solution = solve(initial_board,listofpoints, Probtype)
print (printable_board(solution, Probtype, listofpoints) if solution else "Sorry, no solution found. :(")

