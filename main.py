#%%
import pygame
import flappyBird
#%%
pygame.init()
pygame.font.init()
#%%
class Game:
	def __init__(self,surface:pygame.Surface):
		self.surface = surface
		self.HEIGHT = self.surface.get_height()
		self.WIDTH = self.surface.get_width()
		self.game = flappyBird.Environment(self.HEIGHT,self.WIDTH)
		self.font = pygame.font.SysFont(None, 36)
	def draw(self,key:bool):
		self.surface.fill((255,255,255))
		pipes,((birdY,birdAngle),),score,dead,paralax = self.game.get(key)
		for length,x in pipes:
			pygame.draw.rect(self.surface,(0,255,0),(x,0,flappyBird.PIPE_SCALE_X,length,))
			pygame.draw.rect(self.surface,(0,255,0),(x,length+flappyBird.PIPE_OFFSET_Y,flappyBird.PIPE_SCALE_X,self.HEIGHT,))

		pygame.draw.rect(self.surface,(255,255,0),(self.WIDTH//2-flappyBird.BIRD_SCALE_X//2,birdY,flappyBird.BIRD_SCALE_X,flappyBird.BIRD_SCALE_Y))

		text =self.font.render(f"{score}",True,(0,0,255))
		self.surface.blit(text,(self.WIDTH//2,self.HEIGHT/20))

def main():
	screen = pygame.display.set_mode((500,700))
	game = Game(screen)
	running = True
	while running:
		key = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				key = True
		
		Game.draw(game,key)#game.draw()
		pygame.display.flip()
		

	return 0

if __name__ == "__main__":
	main()