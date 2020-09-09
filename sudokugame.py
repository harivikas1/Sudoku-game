import pygame
import time
from sudoku import Sudoku
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class cube:
	def __init__(self,value,row,col,sizex,sizey):
		self.value=value;
		self.temp=0;
		self.row=row
		self.col=col
		self.sizex=sizex
		self.sizey=sizey
		self.selected=False;


	def  draw_rect(self,win):
		font=pygame.font.SysFont("cambria",40)
		x=(self.col)*(self.sizex);
		y=(self.row)*(self.sizey);
		gap=self.sizex;
		
		if(self.temp!=0 and self.value==0):
			text=font.render(str(self.temp),1,GREY)
			win.blit(text, (x + (gap/4 - text.get_width()/2), y + (gap/4 - text.get_height()/2)))

		elif (self.value!=0):
			text=font.render(str(self.value),1,BLACK)
			win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

		if self.selected==True:
			pygame.draw.rect(win,RED,(x,y,self.sizex,self.sizey),3)

			
class grid:
	"""board = [
		 [3, 0, 6, 5, 0, 8, 4, 0, 0], 
         [5, 2, 0, 0, 0, 0, 0, 0, 0], 
         [0, 8, 7, 0, 0, 0, 0, 3, 1], 
         [0, 0, 3, 0, 1, 0, 0, 8, 0], 
         [9, 0, 0, 8, 6, 3, 0, 0, 5], 
         [0, 5, 0, 0, 9, 0, 6, 0, 0], 
         [1, 3, 0, 0, 0, 0, 2, 5, 0], 
         [0, 0, 0, 0, 0, 0, 0, 7, 4], 
         [0, 0, 5, 2, 0, 6, 3, 0, 0]
	]"""

	board=Sudoku(3).difficulty(0.5).board

	for i in range(9):
		for j in range(9):
			if board[i][j]==None:
				board[i][j]=0

	def __init__(self,row,col,width,height):
		self.row=row
		self.col=col
		self.width=width
		self.height=height
		self.sizex=width//row;
		self.sizey=height//col;
		self.cubes=[[cube(self.board[i][j],i,j,self.sizex,self.sizey) for j in range(self.col)] for i in range(self.row)]
		self.selected=None
		

	def get_selected(self,pos):
		x,y=pos;
		if(x<self.width and y<self.height):
			x=x//self.sizex;
			y=y//self.sizey;
			if(self.selected):
				x1,y1=self.selected;
				self.cubes[x1][y1].selected=False;

			self.cubes[y][x].selected=True;
			self.selected=(y,x);
			return (y,x);
		return None

	
	def draw_grid(self,win):
		for j in range(self.row+1):
			thick=1;
			if(j%3 == 0):
				thick=3;

			pygame.draw.line(win,BLACK,(0,j*self.sizey),(self.height,j*self.sizey),thick)

		for i in range(self.col+1):
			thick=1;
			if(i%3 == 0):
				thick=3;
			pygame.draw.line(win,BLACK,(i*self.sizex,0),(i*self.sizex,self.width),thick)



def draw_sudoku(win,sudoku,run_time,wrongattempts):
	win.fill(WHITE);
	for i in range(len(sudoku.cubes)):
		for j in range(len(sudoku.cubes[i])):
			sudoku.cubes[i][j].draw_rect(win);

	sudoku.draw_grid(win);
	fnt = pygame.font.SysFont("comicsans", 40)
	minute=run_time//60
	text = fnt.render("Time: " + str(int(minute))+":"+ str(int(run_time%60)), 1, BLACK)
	win.blit(text, (400, 560))

	font = pygame.font.SysFont('cambria', 40) 
	text = fnt.render("X "+str(wrongattempts), 1, RED);
	win.blit(text, (20, 560))

	pygame.display.update()

def issafe(board,val,pos):
	x,y=pos
	for i in range(len(board)):
		if(board[i][y]==val):
			return False

	for j in range(len(board[0])):
		if(board[x][j]==val):
			return False

	xl=(x//3)*3;
	yl=(y//3)*3;

	for i in range(xl,xl+3):
		for j in range(yl,yl+3):
			if board[i][j]==val:
				return False

	return True

def solve(board):
	pos=None;
	for i in range(len(board)):
		for j in range(len(board[0])):
			if(board[i][j]==0):
				pos=(i,j)
	if not pos:
		return True;
	x,y=pos
	for i in range(1,10):
		if issafe(board,i,pos):
			board[x][y]=i;
			if(solve(board)):
				return True
	board[x][y]=0;
	return False;

	


def main():
	pygame.init()
	win=pygame.display.set_mode((540,600))
	pygame.display.set_caption("Sudoku Game");
	sudoku=grid(9,9,540,540);
	run=True;
	key=None;
	start=time.time();
	wrongattempts=0;
	

	while(run):
		run_time=time.time()-start;
		draw_sudoku(win,sudoku,run_time,wrongattempts)

		for event in pygame.event.get():

			if event.type==pygame.QUIT:
				run=False;

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos=pygame.mouse.get_pos()
				if (sudoku.get_selected(pos)):
					key=None


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
						key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9

				if event.key==pygame.K_DELETE:
					if(sudoku.selected):
						x,y=sudoku.selected
						sudoku.cubes[x][y].temp=0;
						key=None;

				if event.key==pygame.K_RETURN:
					i,j =sudoku.selected
					solvable=False;
					if(sudoku.cubes[i][j].temp!=0):
						if(sudoku.cubes[i][j].value==0):
							tempgrid = [[sudoku.cubes[x][y].value for y in range(sudoku.col)] for x in range(sudoku.row)]
							if(issafe(tempgrid,sudoku.cubes[i][j].temp,(i,j))):
								tempgrid[i][j]=sudoku.cubes[i][j].temp
								if(solve(tempgrid)):
									sudoku.cubes[i][j].value=(sudoku.cubes[i][j].temp)
									print("correct")
									solvable=True
									
					if not solvable:
						sudoku.cubes[i][j].temp=0;
						wrongattempts+=1
						key=None
						print("wrong :",wrongattempts)

				if event.key==pygame.K_SPACE:
					tempgrid = [[sudoku.cubes[x][y].value for y in range(sudoku.col)] for x in range(sudoku.row)]
					solve(tempgrid)
					for i in range(9):
						for j in range(9):
							sudoku.cubes[i][j].value=tempgrid[i][j];

					print("solved")

		if sudoku.selected and key!=None:
			x,y=sudoku.selected
			sudoku.cubes[x][y].temp=key;

		
		
	pygame.QUIT; 

main();


