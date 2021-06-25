#%%
from flappyBird import Bird, PIPE_DISTANCE
import neat
import pygame
import numpy as np
from game import Game
import os
import pickle
#%%
font = pygame.font.SysFont("arial", 50)
generation = 0
minimum = False
text_mode = False
def compute_population(genomes,config):
	global generation,minimum,text_mode
	screen = pygame.display.set_mode((700,800))
	game_screen = pygame.Surface((500,700))
	running = True
	clock = pygame.time.Clock()
	nets = []
	birds = []
	
	for idx, genome in genomes:

		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		genome.fitness = 0
		birds.append(Bird(game_screen.get_height()))


	game = Game(game_screen,birds)
	while running:
		if minimum or text_mode:
			clock.tick(10000000)
		else:
			clock.tick(60)	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type ==pygame.KEYDOWN:
				if event.key == pygame.K_m:
					minimum = not minimum
					continue
				if event.key == pygame.K_t:
					text_mode = not text_mode

		
		closest_pipe = game.game.closest_pipe
		key = [(net.activate(np.array([*closest_pipe,*birds[idx].bird_top_bottom])))[0]>0.5 if not birds[idx].dead else False for idx,net in enumerate(nets)]
		#print(key)
		if not text_mode:
			dead = game.draw(key,clock,minimum)
			screen.blit(game_screen,(0,100))
		else:
			game.game.compute_next(key)
			dead = np.all(game.game.result[3])
		if dead: break 

		res = game.game.result

		for idx,bird in enumerate(birds):
			genomes[idx][1].fitness = bird.score

		text = font.render(f"GEN{generation},score={res[2]},FPS={clock.get_fps():.0f}",True,(255,255,255))
		screen.blit(text,(10,10))
		pygame.display.update()
		
		screen.fill((0,0,0))	




	generation+=1

def save(something,*path):
	return pickle.dump(something,open(os.path.join(*path),'wb'))


def main(file=os.path.join("neat_stuff","best.pkl"),max_gens=10):
	config_path = os.path.join("neat_stuff", "config-feedforward.txt")
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	population = neat.Population(config)

	population.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	population.add_reporter(stats)
	population.run(compute_population,max_gens)
	
	if isinstance(file,str):file = file,
	
	
	save(population.best_genome,*file)








if __name__ == '__main__':
	main()