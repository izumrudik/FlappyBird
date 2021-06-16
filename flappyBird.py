BIRD_SCALE_X = 50
BIRD_SCALE_Y = 40
PIPE_SCALE_X = 50
PIPE_OFFSET_Y = 100
PIPE_DISTANCE = 200
import numpy as np
from random import randint
class FlappyBird:
	def __init__(self,screen_HEIGHT:int,screen_WIDTH:int,):
		self._WIDTH = screen_WIDTH
		self._HEIGHT = screen_HEIGHT
		self.__pipesX = np.array([self._WIDTH],dtype="int32")
		self.__pipesY = np.array([randint(0,self._HEIGHT-PIPE_OFFSET_Y)],dtype="int32")
		self.__birdY = self._HEIGHT//2
		self.__birdAngle = 0
		self.__score = 0
		self.__dead = False
		self.__Y = 0
		
	def get(self, key:bool=False):
		"""
		returns a tuple of:
		({
			(length of pipe from top, it's x position to left edge)
			,...},

		(bird's top left corner's x,
			bird's angle(0 is normal, <0 is more to the top, >0 is more to the bottom)
		),
		score:int,
		dead:bool,
		y for paralax background:int)
		"""
		#move bird
		self.__birdAngle+=1
		self.__birdY = min(self.__birdY+5,self._HEIGHT-BIRD_SCALE_Y)# +5 or hit the ground
		#see if we died
		if self.__dead:
			return set(zip(self.__pipesY,self.__pipesX)),(self.__birdY,self.__birdAngle),self.__score,True,self.__Y//20

		#all pipes right to the bird
		pipesBefore = self.__pipesX[self.__pipesX+PIPE_SCALE_X >= self._WIDTH//2 - BIRD_SCALE_X//2]
		
		#move pipes & background
		self.__Y+=1
		if self.__Y %10 == 0:
			self.__pipesX-=1
			#collision
			bird = (self._WIDTH//2-BIRD_SCALE_X//2,self.__birdY,BIRD_SCALE_X,BIRD_SCALE_Y,self.__birdAngle)
			pipesTop = (self.__pipesX,0,PIPE_SCALE_X,self.__pipesY)
			pipesBottom = (self.__pipesX,self.__pipesY+PIPE_OFFSET_Y,PIPE_SCALE_X,self._HEIGHT)
			
			colides = False
			if colides:
				self.__dead = True

			#score
			if (pipesBefore+PIPE_SCALE_X <= self._WIDTH//2 - BIRD_SCALE_X//2).any():
				self.__score+=1


		#remove pipes
		mask = self.__pipesX<0
		self.__pipesX = np.delete(self.__pipesX,mask)
		self.__pipesY = np.delete(self.__pipesY,mask)
		#generate pipes
		if self._WIDTH-np.max(self.__pipesX) >= PIPE_DISTANCE:
			self.__pipesX = np.append(self.__pipesX,self._WIDTH)
			self.__pipesY = np.append(self.__pipesY,randint(0,self._HEIGHT-PIPE_OFFSET_Y))



		return set(zip(self.__pipesY,self.__pipesX)),(self.__birdY,self.__birdAngle),self.__score,False,self.__Y//20

	def __call__(self, *args, **kwds):
		return self.get(*args, **kwds)