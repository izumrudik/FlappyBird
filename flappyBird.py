#%%
BIRD_SCALE_X = 18*3//18*18
BIRD_SCALE_Y = int(BIRD_SCALE_X/18*12)
PIPE_SCALE_X = 50
PIPE_OFFSET_Y = 200
PIPE_DISTANCE = 200
#%%
import numpy as np
from random import randint
from typing import Optional,List
#%%
def FlappyBird(*args, **kwargs):
	return Environment(*args, **kwargs)
#%%
class Environment:
	def __init__(self,screen_HEIGHT:int,screen_WIDTH:int,birds:"Optional[List[Bird]]"=None,):
		self._WIDTH = screen_WIDTH
		self._HEIGHT = screen_HEIGHT
		self.__pipesX = np.array([self._WIDTH],dtype="int32")
		self.__pipesY = np.array([randint(0,self._HEIGHT-PIPE_OFFSET_Y)],dtype="int32")
		if birds is None:
			birds = [Bird(self._HEIGHT)]
		self.__birds = birds
		self.__score = 0
		self.__X = 0
		self.__dead = [False for _ in self.__birds]

	def get(self, key:"bool|List[bool]"=False):
		"""
		returns a tuple of:
		({
			(length of pipe from top, it's x position to left edge)
			,...},

		[(bird's top left corner's x,
			bird's angle°(0 is normal, <0 is more to the top, >0 is more to the bottom)
		)],
		score:int,
		dead:bool,
		y for paralax background:int)
		"""
		if isinstance(key,bool):
			key = [key]
		pipe = None
		left_to_the_bird = self.__pipesX[self.__pipesX <= self._WIDTH//2 + BIRD_SCALE_X//2]
		if len(left_to_the_bird) !=0:
			idx_max = np.argmax(left_to_the_bird)
			if self.__pipesX[idx_max]+PIPE_SCALE_X>self._WIDTH//2 - BIRD_SCALE_X//2:
				pipe = self.__pipesY[idx_max]

		birds_returns = [bird.get(pipe,key[idx]) for idx,bird in enumerate(self.__birds)]


		self.__dead = [b.dead for b in self.__birds]
		if np.all(self.__dead):
			return set(zip(self.__pipesY,self.__pipesX)),birds_returns,self.__score,[True for _ in self.__birds],self.__X//20

		#move bird
		#all pipes right-> to the bird
		pipesBefore = self.__pipesX[self.__pipesX+PIPE_SCALE_X >= self._WIDTH//2 - BIRD_SCALE_X//2]
		
		#move pipes & background
		self.__X+=1
		self.__pipesX-=1

			#score
		if (pipesBefore+PIPE_SCALE_X <= self._WIDTH//2 - BIRD_SCALE_X//2).any():
			self.__score+=1


		#remove pipes
		mask = self.__pipesX< -PIPE_SCALE_X
		self.__pipesX = np.delete(self.__pipesX,mask)
		self.__pipesY = np.delete(self.__pipesY,mask)
		#generate pipes
		if self._WIDTH-np.max(self.__pipesX) >= PIPE_DISTANCE:
			self.__pipesX = np.append(self.__pipesX,self._WIDTH)
			self.__pipesY = np.append(self.__pipesY,randint(0,self._HEIGHT-PIPE_OFFSET_Y))



		return set(zip(self.__pipesY,self.__pipesX)),birds_returns,self.__score,[bird.dead for bird in self.__birds],self.__X//20
###
	def __call__(self, *args, **kwds):
		return self.get(*args, **kwds)
	@property
	def dead(self):
		return self.__dead
#%%
class Bird:
	def __init__(self,height):
		self._HEIGHT = height
		self.__velocity = 0
		self.__dead = False
		self.__birdAngle = 0
		self.__y = height//2 - BIRD_SCALE_Y//2
		self.__score = 0
		self.__frames_from_last_key = 0
	def get(self,pipe_length:int,key:bool):
		"""
		returns a tuple of:
		bird's top left corner's x,
		bird's angle°(0 is normal, <0 is more to the top, >0 is more to the bottom)
		"""
		if self.dead:
			return (self.__y,self.__birdAngle)
		#if key pressed
		if key:
			self.__velocity = -10.5
			self.__frames_from_last_key=0

		self.__frames_from_last_key+=1
		#calculate position
		speed = min(8,max(-6,self.__velocity*(self.__frames_from_last_key) + .5*(self.__frames_from_last_key)**2))
		self.__y = max(0,min(self._HEIGHT-BIRD_SCALE_Y,self.__y+speed,),)# +5 or hit the ground


		#see if we collide
		if pipe_length is None:
			return (round(self.__y),round(self.__birdAngle))
		
		if (pipe_length>=self.__y or #top
		   pipe_length+PIPE_OFFSET_Y <= self.__y + BIRD_SCALE_Y):
		   self.__dead = True

		return (round(self.__y),round(self.__birdAngle))

###
	def __call__(self, *args, **kwds):
		return self.get(*args, **kwds)
	@property
	def dead(self)->bool:
		return self.__dead
	@property
	def score(self)->int:
		return self.__score