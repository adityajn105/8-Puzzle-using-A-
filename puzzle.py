from random import shuffle
import curses


class Puzzle:
    def __init__(self,config=None):
        if config==None:
            self.config=self.generateRandomConfig()
        else:
            self.config=config
        self.state=self.generateState()
        self.ans = [[1,2,3],[4,5,6],[7,8," "]]

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
        """.format(self.state[0][0],
                   self.state[0][1],
                   self.state[0][2],
                   self.state[1][0],
                   self.state[1][1],
                   self.state[1][2],
                   self.state[2][0],
                   self.state[2][1],
                   self.state[2][2])

    def generateState(self,conf=None):
        if conf==None:
            conf=self.config
        state=[[0,0,0],[0,0,0],[0,0,0]]
        for i in range(0,3):
            for j in range(0,3):
                state[i][j]=conf[i*3+j]
        return state

    def move_tile(self,ch):
        pos=self.findBlank()
        if ch=="up":
            if pos[0]!=0:
                self.swap(pos[0],pos[1],pos[0]-1,pos[1])
        elif ch=="down":
            if pos[0]!=2:
                self.swap(pos[0],pos[1],pos[0]+1,pos[1])
        elif ch=="left":
            if pos[1]!=0:
                self.swap(pos[0],pos[1],pos[0],pos[1]-1)
        elif ch=="right":
            if pos[1]!=2:
                self.swap(pos[0],pos[1],pos[0],pos[1]+1)

    def swap(self,i1,j1,i2,j2):
        self.state[i1][j1],self.state[i2][j2]=self.state[i2][j2],self.state[i1][j1]
        self.config=self.stateToConfig(self.state)

    def findBlank(self):
        for i in range(0,3):
            for j in range(0,3):
                if self.state[i][j]==" ":
                    return (i,j)


    def printControls(self):
        return """
                    \u2191  -> Move Up
                    \u2193  -> Move Down
                    \u2190  -> Move Left
                    \u2192  -> Move Right
                     n  -> New Puzzle
        """

    def __eq__(self, board):
        for i in range(0,9):
            if self.board[i]!=self.config[i]:
                return False
        return True

    def isSolution(self):
        for i in range(0,3):
            for j in range(0,3):
                if self.ans[i][j]!=self.state[i][j]:
                    return False
        return True

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




                Press \u21b3 (ENTER Key) to begin new Game





        """

    def stateToConfig(self,state):
        conf=[0,0,0,0,0,0,0,0,0]
        for i in range(0,3):
            for j in range(0,3):
                conf[i*3+j]=state[i][j]
        return conf

    def manhattenDistance(self,state):
    	dis=0
    	for i in range(3):
    		for j in range(3):
    			if not state[i][j]==" ":
    				row=(state[i][j]-1)/3
    				col=(state[i][j]-1)%3
    				dis=dis+abs(row-i)+abs(col-j)
    	return dis

    def generateRandomConfig(self):
        x = list(range(0,9))
        x[0]=" "
        shuffle(x)
        return x

def initialize(window):
    board = Puzzle([1,2,3,4,8,5,7," ",6])
    window.insstr(0, 0, str(board))
    window.insstr(15,0,board.printControls())
    ch = window.getch()
    while str(ch)!='10':
        if ch==curses.KEY_UP:
            board.move_tile("up");
        elif ch==curses.KEY_DOWN:
            board.move_tile("down")
        elif ch==curses.KEY_LEFT:
            board.move_tile("left")
        elif ch==curses.KEY_RIGHT:
            board.move_tile("right")
        elif ch==ord("n"):
            board =Puzzle(None)

        if board.isSolution():
            window.insstr(0,0,board.getvictorySign(),curses.A_BLINK)
        else:
            window.insstr(0,0,str(board))
            window.insstr(15, 0, board.printControls())
        ch = window.getch()
        window.refresh()

if __name__=='__main__':
    curses.wrapper(initialize)