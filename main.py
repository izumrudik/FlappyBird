#%%
import pygame
import flappyBird
#%%
class Game:
	def __init__(self,surface:pygame.Surface):
		self.surface = surface
		self.HEIGHT = self.surface.get_height()
		self.WIDTH = self.surface.get_width()
		self.game = flappyBird.FlappyBird(self.HEIGHT,self.WIDTH)
	def draw(self):
		self.surface.fill((255,255,255))
		pipes,(birdY,birdAngle),score,dead,paralax = self.game.get(False)
		#bird
		pygame.draw.rect(self.surface,(255,255,0),(self.WIDTH//2-flappyBird.BIRD_SCALE_X,birdY,flappyBird.BIRD_SCALE_X,flappyBird.BIRD_SCALE_Y))
		print(score)
		for length,x in pipes:
			pygame.draw.rect(self.surface,(0,255,0),(x,0,flappyBird.PIPE_SCALE_X,length,))
			pygame.draw.rect(self.surface,(0,255,0),(x,length+flappyBird.PIPE_OFFSET_Y,flappyBird.PIPE_SCALE_X,self.HEIGHT,))


def main():
	screen = pygame.display.set_mode((500,700))
	game = Game(screen)
	running = True
	while running:
		for event in pygame.event.get():
			if event == pygame.QUIT:
				running = False
				quit()
		Game.draw(game)#game.draw()
		pygame.display.flip()
		

	return 0

if __name__ == "__main__":
	main()