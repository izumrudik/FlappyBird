from flappyBird import Bird
import os
import pickle
import pygame
from game import Game
import neat
from typing import List
import numpy as np
def load(*file):
	return pickle.load(open(os.path.join(*file),'rb'))


def main(file:"str|List[str]"=["neat_stuff","best.pkl"]):
	if isinstance(file,str):file = file,
	genome = load(*file)
	config_path = os.path.join("neat_stuff", "config-feedforward.txt")
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	net = neat.nn.FeedForwardNetwork.create(genome, config)

	#neat stuff

	running = True
	screen = pygame.display.set_mode((500,700))
	bird = Bird(screen.get_height())
	game = Game(screen,[bird])
	
	clock = pygame.time.Clock()
	while running:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		closest_pipe = game.game.closest_pipe
		key = (net.activate(np.array([*closest_pipe,*bird.bird_top_bottom])))[0]>0.5
		if game.draw(key,clock):
			bird = Bird(screen.get_height())
			game = Game(screen,[bird])
	
		pygame.display.flip()



		






if __name__ == '__main__':
	main()
