#%%
import pygame
import flappyBird
import numpy as np
from os.path import join
from typing import Optional,List
#%%
pygame.init()
pygame.font.init()
#%%
BIRD_SPRITES = [
pygame.transform.scale(pygame.image.load(join("images","bird1.png")),
				(flappyBird.BIRD_SCALE_X,
				 flappyBird.BIRD_SCALE_Y)
),
pygame.transform.scale(pygame.image.load(join("images","bird2.png")),
				(flappyBird.BIRD_SCALE_X,
				 flappyBird.BIRD_SCALE_Y)
),
pygame.transform.scale(pygame.image.load(join("images","bird3.png")),
				(flappyBird.BIRD_SCALE_X,
				 flappyBird.BIRD_SCALE_Y)
),
]

PIPE_TOP_SPRITE = pygame.image.load(join("images","pipe.png"))
PIPE_TOP_SPRITE = pygame.transform.scale(PIPE_TOP_SPRITE,
				(flappyBird.PIPE_SCALE_X,
				 PIPE_TOP_SPRITE.get_height())
)
PIPE_TOP_SPRITE = pygame.transform.flip(PIPE_TOP_SPRITE,True,False)
PIPE_BOTTOM_SPRITE = pygame.transform.flip(PIPE_TOP_SPRITE,False,True)
BG_SPRITE = pygame.image.load(join("images","bg.png"))
BG_SPRITE = pygame.transform.scale(BG_SPRITE,BG_SPRITE.get_rect(height=700).size)
BG_WIDTH = BG_SPRITE.get_width()
#%%
class Game:
	def __init__(self,surface:pygame.Surface,birds:Optional[List[flappyBird.Bird]]=None):
		self.surface = surface
		self.HEIGHT = self.surface.get_height()
		self.WIDTH = self.surface.get_width()
		self.game = flappyBird.FlappyBird(self.HEIGHT,self.WIDTH,birds
		)
		
		self.font = pygame.font.SysFont("", self.HEIGHT//20)
	def draw(self,key:"List[bool]|bool",clock:pygame.time.Clock,minimum:bool=False):
		self.surface.fill((255,255,255))
		self.game.compute_next(key)
		pipes,birds,score,dead,paralax = self.game.result


		if not minimum:
			x =  -(paralax/2%BG_WIDTH)
			while x<self.WIDTH:
			
				self.surface.blit(BG_SPRITE,BG_SPRITE.get_rect(topleft=(x,0)))
				x += BG_WIDTH



		bird_sprite = BIRD_SPRITES[paralax//20%3]
		alive_birds = 0
		for idx,bird in enumerate(birds):
			birdY,birdAngle = bird.result
			if bird.dead:continue
			if not minimum and alive_birds > 9: continue
			if not bird.dead: alive_birds+=1
			if not minimum:
				bird_sprite_new = pygame.transform.rotate(bird_sprite,-birdAngle)

			rect = (bird_sprite_new.get_rect(center=(self.WIDTH//2,birdY+flappyBird.BIRD_SCALE_Y//2,))
			)
			if not minimum:
				rect.move(-pygame.math.Vector2(-flappyBird.BIRD_SCALE_X//2,0).rotate(birdAngle))
		
			self.surface.blit(
				bird_sprite_new,
				rect
			)

		#pygame.draw.rect(self.surface,(255,0,0,),rect,5)
		#t1,t2 = temp
		#pygame.draw.line(self.surface,(0,255,0,),(rect.left,t1),(rect.right,t1),5)
		#pygame.draw.line(self.surface,(0,0,255,),(rect.left,t2),(rect.right,t2),5)

		for idx,(length,x) in enumerate(pipes):
			if minimum and idx>0: break

			self.surface.blit(PIPE_BOTTOM_SPRITE,
				PIPE_BOTTOM_SPRITE.get_rect(
					bottomleft=(x,length,)
					)
			)
			self.surface.blit(PIPE_TOP_SPRITE,
				PIPE_TOP_SPRITE.get_rect(
					topleft=(x,length+flappyBird.PIPE_OFFSET_Y)
					)
			) 

		text =self.font.render(f"{score}",True,(255,0,255))
		self.surface.blit(text,(self.WIDTH//2,self.HEIGHT//20))
		text =self.font.render(f"FPS:{clock.get_fps():.0f}",True,(255,0,255))
		self.surface.blit(text,(self.WIDTH//2,self.HEIGHT//20+36))
		return np.all(dead)
def main():
	screen = pygame.display.set_mode((500,700))
	game = Game(screen)
	running = True
	clock = pygame.time.Clock()
	minimum = False
	while running:
		clock.tick(60)
		key = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type ==pygame.KEYDOWN:
				if event.key == pygame.K_m:
					minimum = not minimum
					continue
			if event.type in (pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN):
				key = True
		

		dead = Game.draw(game,key,clock,minimum)#game.draw(key,clock,minimum)
		if dead and key:
			game = Game(screen)
		pygame.display.flip()

	return 0

if __name__ == "__main__":
	main()