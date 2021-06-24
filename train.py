#%%
from flappyBird import Bird
import neat
import pygame
import numpy as np
from game import Game
import os
import pickle
#%%


def compute_population(genomes,config):
	screen = pygame.display.set_mode((800,800))
	game_screen = pygame.Surface((500,700))
	running = True
	clock = pygame.time.Clock()
	minimum = False
	nets = []
	birds = []
	for idx, genome in genomes:

		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		genome.fitness = 0
		birds.append(Bird(game_screen.get_height()))




	game = Game(screen,birds)
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
				key = True
				continue
			elif event.type == pygame.MOUSEBUTTONDOWN:
				key = True
		

		dead = game.draw(key,clock,minimum)
		if dead: break 
		pygame.display.flip()
	pygame.display.quit()

def save(something,*path):
	return pickle.dump(something,open(os.path.join("neiro",*path),'wb'))


def main(file=os.path.join("neat_stuff","best.pkl"),max_gens=10):
	config_path = os.path.join("neat_stuff", "config-feedforward.txt")
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	population = neat.Population(config)

	population.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	population.add_reporter(stats)
	population.run(compute_population,max_gens)









if __name__ == '__main__':
	main()