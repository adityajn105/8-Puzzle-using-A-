from random import shuffle
from queue import PriorityQueue
import curses
import time


class Puzzle(object):
	def __init__(self,board=None,moves=0,previous=None):
		if board==None:
			self.board=self.generateRandomboard()
		else:
			self.board=board
		self.moves=moves
		self.previous=previous

	def generateRandomboard(self):
		x = list(range(0,9))
		x[0]=" "
		shuffle(x)
		return x

	def __str__(self):
		return """

	            |=======|=======|=======|
	            |       |       |       |
	            |   {}   |   {}   |   {}   |
	            |       |       |       |
	            |=======|=======|=======|
	            |       |       |       |
	            |   {}   |   {}   |   {}   |
	            |       |       |       |
	            |=======|=======|=======|
	            |       |       |       |
	            |   {}   |   {}   |   {}   |
	            |       |       |       |
	            |=======|=======|=======|
	    
	            	moves : {}
	    """.format(self.board[0],
	    	self.board[1],
	    	self.board[2],
	    	self.board[3],
	    	self.board[4],
	    	self.board[5],
	    	self.board[6],
	    	self.board[7],
	    	self.board[8],
	    	self.moves)

	def __eq__(self,other):
		"""
			check equality of self with other
		"""
		if other==None:
			return False
		return self.board==other.board

	def isSolution(self):
		"return True if current board is goal"
		return self.board==[1,2,3,4,5,6,7,8,' ']

	def manhattendistance(self):
		dist = 0
		for i in range(0,9):
			if self.board[i] == " ":
				rowd = abs(2 - int(i/3))
				cold = abs(2 - i%3)
				dist += (rowd+cold)
			else:
				rowd = abs(int((self.board[i]-1)/3) - int(i/3))
				cold = abs((self.board[i]-1)%3 - i%3)
				dist += abs(rowd+cold)
		return dist

	def move_tile(self,directn):
		"""
			1 2 3
			4 5 6
			7 8 9

		"""
		pos_blank = self.find_blank()

		if directn=="up":
			if pos_blank > 3:
				self.exchange(pos_blank-1,pos_blank-4)
		elif directn=="left":
			if pos_blank%3 != 1:
				self.exchange(pos_blank-1,pos_blank-2)
		elif directn=="right":
			if pos_blank%3 != 0:
				self.exchange(pos_blank-1,pos_blank)
		else:
			if pos_blank < 7:
				self.exchange(pos_blank-1,pos_blank+2)

	def exchange(self,i,j):
		self.board[i],self.board[j] = self.board[j],self.board[i]

	def find_blank(self):
		for i in range(0,9):
			if self.board[i]==" ":
				return i+1

	def clone(self):
		return Puzzle(board = self.board.copy(),moves=self.moves+1,previous=self)


	def getNeighbors(self):
		neighbors = []
		pos_blank = self.find_blank()

		if pos_blank > 3:
			new_board = self.clone()
			new_board.move_tile("up")
			neighbors.append(new_board)

		if pos_blank%3 != 1:
			new_board = self.clone()
			new_board.move_tile("left")
			neighbors.append(new_board)

		if pos_blank%3 != 0:
			new_board = self.clone()
			new_board.move_tile("right")
			neighbors.append(new_board)

		if pos_blank < 7:
			new_board = self.clone()
			new_board.move_tile("down")
			neighbors.append(new_board)

		return neighbors


	def getvictorySign(self):
		return """





		                |=======================|
		                |                       |
		                |                       |
		                |                       |
		                |       You Won!!       |
		                |                       |
		                |                       |
		                |                       |
		                |=======================|






		        	Press \u21b3 (ENTER Key) to Exit







		"""

	def printControls(self):
		return """
		            \u2191  -> Move Up
		            \u2193  -> Move Down
		            \u2190  -> Move Left
		            \u2192  -> Move Right
		             x  -> Declare Non Solvable
		             n  -> New Puzzle
		             a  -> Automate
		"""

	def totalInversions(self):
		"""
		odd no of inversions means problem is not solvable
		"""
		inversions = 0
		nboard = self.board.copy()
		nboard.remove(' ')
		for i in range(0,8):
			for j in range(i+1,8):
				if nboard[i]>nboard[j]:
					inversions+=1
		return inversions


	def in_priority_queue(self,count):
		"""
		count is used in case 1st entry of tuple is equal
		priorityqueue uses 2nd entry of tuple in case 1st entry is equal
		third entry is puzzle which cant be compared
		"""
		return (self.manhattendistance()+self.moves,count,self)


def automate(board,window):
	queue = PriorityQueue()
	if board.totalInversions()%2==1:
		window.clear()
		window.insstr(0,0,
			"""
			____________________________
			|  Problem is not Solvable |
			|     (Odd Inversions)     |	
			----------------------------
			""")
		window.refresh()
		time.sleep(1)
		window.getch()
		return 

	queue.put(board.in_priority_queue(0))

	path = []
	i=1
	while not queue.empty():
		bestboard = queue.get()[2]
		if not bestboard.isSolution():
			for neighbor in bestboard.getNeighbors():
				if neighbor != bestboard.previous:
					queue.put(neighbor.in_priority_queue(i))
					i+=1
		else:
			path.append(bestboard)
			prev = bestboard.previous
			while prev is not None:
				path.append(prev)
				prev = prev.previous
			break

	path.reverse()
	for board in path:
		window.clear()
		window.insstr(0,0,str(board))
		window.refresh()
		time.sleep(1.5)

	window.insstr(18, 0, "\t\tPress \u21b3 (ENTER Key) to Continue" )
	window.refresh()
	window.getch()

def initialize(window):
	board = Puzzle([1,2,3,4,5,6,' ',8,7])
	window.insstr(0, 0, str(board))
	window.insstr(18,0,board.printControls())
	ch = window.getch()
	while str(ch)!='10':
		if ch==curses.KEY_UP:
			board.move_tile("up");
			board.moves+=1
		elif ch==curses.KEY_DOWN:
			board.move_tile("down")
			board.moves+=1
		elif ch==curses.KEY_LEFT:
			board.move_tile("left")
			board.moves+=1
		elif ch==curses.KEY_RIGHT:
			board.move_tile("right")
			board.moves+=1
		elif ch==ord("n"):
			board =Puzzle(None)
		elif ch == ord("x"):
			window.clear()
			if board.totalInversions()%2==1:
				window.insstr(0,0,board.getvictorySign())
				board = Puzzle()
			else:
				window.insstr(0,0,
				"""
			____________________________
			|   Problem is solvable!!  |
			----------------------------

			Press \u21b3 (ENTER Key) to Continue
				""")
			window.refresh()
			window.getch()
		elif ch == ord("a"):
			window.clear()
			window.insstr(0,0,
				"""
			____________________________
			|Searching Optimal Solution|
			----------------------------
				""")
			window.refresh()
			time.sleep(1)
			automate(board,window)
			board = Puzzle(None)

		window.clear()
		if board.isSolution():
			window.insstr(0,0,board.getvictorySign())
		else:
			window.insstr(0, 0, str(board))
			window.insstr(18, 0, board.printControls())
		ch = window.getch()
		window.refresh()


if __name__=='__main__':
	curses.wrapper(initialize)