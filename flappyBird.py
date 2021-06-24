#%%
BIRD_SCALE_X = 18*3
BIRD_SCALE_Y = 12*3
PIPE_SCALE_X = 50
PIPE_OFFSET_Y = 300
PIPE_DISTANCE = 200
#%%
import numpy as np
from random import randint
from typing import Optional,List,Tuple,Set
from math import sqrt,sin,cos,atan as arctg,pi as Pi,radians
from functools import cache
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

	def compute_next(self, key:"bool|List[bool]")-> None:
		"""
		returns a tuple of:
		({
			(length of pipe from top, it's x position to left edge)
			,...},

		[(bird's top side's y,
			bird's angle°(0 is normal, <0 is more to the top, >0 is more to the bottom)
		)],
		score:int,
		dead:bool,
		y for paralax background:int)
		"""


		if isinstance(key,bool):
			key = [key]


		pipe:Optional[int] = None
		left_to_the_bird = self.__pipesX[self.__pipesX <= self._WIDTH//2 + BIRD_SCALE_X//2]
		if len(left_to_the_bird) !=0:
			idx_max = np.argmax(left_to_the_bird)
			if self.__pipesX[idx_max]+PIPE_SCALE_X>self._WIDTH//2 - BIRD_SCALE_X//2:
				pipe = self.__pipesY[idx_max]

		for idx,bird in enumerate(self.__birds):
			bird.compute_next(pipe,key[idx],self.score) 


		self.__dead = [b.dead for b in self.__birds]
		if np.all(self.__dead):
			return 

		#move bird
		#all pipes right-> to the bird
		right_to_the_bird = self.__pipesX[self.__pipesX+PIPE_SCALE_X >= self._WIDTH//2 - BIRD_SCALE_X//2]
		
		#move pipes & background
		self.__X+=1
		self.__pipesX-=1

			#score
		if (right_to_the_bird+PIPE_SCALE_X <= self._WIDTH//2 - BIRD_SCALE_X//2).any():
			self.__score+=1


		#remove pipes
		mask = self.__pipesX< -PIPE_SCALE_X
		self.__pipesX = np.delete(self.__pipesX,mask)
		self.__pipesY = np.delete(self.__pipesY,mask)
		#generate pipes
		if self._WIDTH-np.max(self.__pipesX) >= PIPE_DISTANCE:
			self.__pipesX = np.append(self.__pipesX,self._WIDTH)
			self.__pipesY = np.append(self.__pipesY,randint(0,self._HEIGHT-PIPE_OFFSET_Y))



###
	@property
	def result(self)-> Tuple[Set[Tuple[int,int]],List[Tuple[int,int]],int,List[bool],int]:
		return set(zip(self.__pipesY,self.__pipesX)),[bird.result for bird in self.__birds],self.__score,self.dead,self.__X
	def __call__(self, *args, **kwds):
		return self.compute_next(*args, **kwds)
	@property
	def dead(self)->List[bool]:
		return self.__dead
	@property
	def score(self)->int:
		return self.__score
	@property 
	def nearest_pipe(self)->Tuple[int,int]:
		right_to_the_bird_mask = self.__pipesX+PIPE_SCALE_X >= self._WIDTH//2 - BIRD_SCALE_X//2
		nearest_pipe_index_after_mask = np.argmin(self.__pipesX[right_to_the_bird_mask])
		return (
			self.__pipesX[right_to_the_bird_mask][nearest_pipe_index_after_mask],
			self.__pipesY[right_to_the_bird_mask][nearest_pipe_index_after_mask]
		)
#%%
@cache
def clamp(min_,max_,num):
	return max(min_,min(max_,num))
@cache
def calculate_фигни(angle):
	другая_фигня = sin(radians(-angle))*BIRD_SCALE_X/2
	angle%=360
	if angle <=90:
		angle+=360
		angle = radians(angle)
		return cos(Pi/2+angle/2-arctg(BIRD_SCALE_X/BIRD_SCALE_Y))*sqrt(1/2*(BIRD_SCALE_X**2+BIRD_SCALE_Y**2)*(1-cos(angle))),другая_фигня	
	elif angle <= 180:
		angle+=270
		angle = radians(angle)
		return (cos(Pi/2+angle/2-arctg(BIRD_SCALE_Y/BIRD_SCALE_X))*sqrt(1/2*(BIRD_SCALE_X**2+BIRD_SCALE_Y**2)*(1-cos(angle)))) - abs(BIRD_SCALE_X-BIRD_SCALE_Y)/2,другая_фигня

	elif angle <=270:
		angle+=180
		angle = radians(angle)
		return cos(Pi/2+angle/2-arctg(BIRD_SCALE_X/BIRD_SCALE_Y))*sqrt(1/2*(BIRD_SCALE_X**2+BIRD_SCALE_Y**2)*(1-cos(angle))),другая_фигня
	else:
		angle+=90
		angle = radians(angle)
		return (cos(Pi/2+angle/2-arctg(BIRD_SCALE_Y/BIRD_SCALE_X))*sqrt(1/2*(BIRD_SCALE_X**2+BIRD_SCALE_Y**2)*(1-cos(angle)))) - abs(BIRD_SCALE_X-BIRD_SCALE_Y)/2,другая_фигня


		

	
class Bird:
	def __init__(self,height):
		self._HEIGHT = height
		self.__dead = False
		self.__angle = 0
		self.__y = height//2 - BIRD_SCALE_Y//2
		self.__score = 0
		self.__frames_from_last_key = 100

	def compute_next(self,pipe_length:Optional[int],key:bool,score:int)-> None:

		if self.dead:
			return 
		self.__score = score
		#if key pressed
		if key:
			self.__frames_from_last_key=0
		self.__frames_from_last_key+=1
		#calculate position
		speed = clamp(-6,7,-10.5*(self.__frames_from_last_key) + .5*(self.__frames_from_last_key)**2)

		if speed<0:
			angspeed = -6
		else:
			angspeed = 5

		self.__angle = clamp(-45,90,self.__angle+angspeed)

		self.__y = self.__y+speed# +speed 



		фигня,другая_фигня = calculate_фигни(-self.__angle)

		self.__y = clamp(0,self._HEIGHT-BIRD_SCALE_Y-другая_фигня+фигня,self.__y)#or hit the ground
		
		BIRD_TOP_Y =    self.__y + фигня + другая_фигня
		BIRD_BOTTOM_Y = self.__y - фигня + другая_фигня + BIRD_SCALE_Y


		


		#see if we collide
		if self._HEIGHT<=BIRD_BOTTOM_Y:
			self.__dead = True
			#self.__angle = 90

		if pipe_length is None:
			return 
		
		if pipe_length>=BIRD_TOP_Y: #top pipe
		   self.__dead = True
		   self.Y = pipe_length
		if pipe_length+PIPE_OFFSET_Y <= BIRD_BOTTOM_Y:#bottom pipe
		   self.__dead = True
		   self.Y = pipe_length+PIPE_OFFSET_Y-BIRD_SCALE_Y

		return

###
	def __call__(self, *args, **kwds):
		return self.compute_next(*args, **kwds)
	@property
	def dead(self)->bool:
		#return False #cheats
		return self.__dead
	@property
	def score(self)->int:
		return self.__score
	@property
	def result(self)-> Tuple[int,int]:
		"""
		returns a tuple of:
		bird's top side's y,
		bird's angle°(0 is normal, <0 is more to the top, >0 is more to the bottom)
		"""
		return (round(self.__y),round(self.__angle))