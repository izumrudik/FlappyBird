#%%
from flappyBird import Bird
import neat
import pygame
import numpy as np
from game import Game
import os
import pickle
#%%
font = pygame.font.SysFont("", 50)
generation = 0
def compute_population(genomes,config):
	global generation
	screen = pygame.display.set_mode((500,800))
	game_screen = pygame.Surface((500,700))
	running = True
	clock = pygame.time.Clock()
	minimum = False
	nets = []
	birds = []
	speed = 600
	for idx, genome in genomes:

		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		genome.fitness = 0
		birds.append(Bird(game_screen.get_height()))



	game = Game(game_screen,birds)
	while running:
		clock.tick(speed)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type ==pygame.KEYDOWN:
				if event.key == pygame.K_m:
					minimum = not minimum
					continue

		
		closest_pipe = game.game.closest_pipe
		key = [(net.activate(np.array([*closest_pipe,*birds[idx].bird_top_bottom])))[0]>0.5 for idx,net in enumerate(nets)]
		#print(key)

		dead = game.draw(key,clock,minimum)
		if dead: break 
		screen.blit(game_screen,(0,100))
		text = font.render(f"{generation=}",True,(255,255,255))
		screen.blit(text,(10,30))
		pygame.display.update()
		
		screen.fill((0,0,0))	






		for idx,bird in enumerate(birds):
			genomes[idx][1].fitness = bird.score
		


	generation+=1

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
	try:iter(file)
	except TypeError: file = (file,)
	save(population.best_genome,*file)








if __name__ == '__main__':
	main()