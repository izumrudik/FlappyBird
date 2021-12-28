
from typing import List

from flappyBird import Bird
import neat
import pygame
import numpy as np
from game import Game
import os
import pickle
from main import resource_path as join
#%%
font = pygame.font.SysFont("arial", 50)
generation = 0
minimum = False
text_mode = False
turbo_mode = False
def compute_population(genomes,config):
	global generation,minimum,text_mode,turbo_mode
	screen = pygame.display.set_mode((700,700))
	game_screen = pygame.Surface((500,700))
	running = True
	clock = pygame.time.Clock()
	nets = []
	birds:List[Bird] = []
	
	for idx, genome in genomes:

		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		genome.fitness = 0
		birds.append(Bird(game_screen.get_height()))

	cool_bird = -1
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
				if event.key == pygame.K_p:
					turbo_mode = not turbo_mode
		
		closest_pipe = game.game.closest_pipe
		
		key = [net.activate(np.array([*closest_pipe,*birds[idx].bird_top_bottom]))[0]>0.5 if not birds[idx].dead else False for idx,net in enumerate(nets)]
		#print(key)
		if not text_mode:
			live = game.draw(key,clock,minimum)
		else:
			game.game.compute_next(key)
			live = np.all(game.game.result[3])
		if live: break 

		res = game.game.result
		live = len(birds)
		for idx,bird in enumerate(birds):
			genomes[idx][1].fitness = bird.score
			if not bird.dead:
				cool_bird = idx
			else: live-=1

		def blit_txt(text:str,x,idx=0):
			if isinstance(text,str):
				text = text.split('\n')
			if len(text)>1:
				blit_txt(text[0],x,idx)
				blit_txt(text[1:],x,idx+1)
				return
			text, = text
			screen.blit(font.render(f"{text}", True, (255, 255, 255)),
                    (x, 10+60*idx))
		if not turbo_mode:
			blit_txt(
f"""GEN{generation}
FPS:{clock.get_fps():.0f}
live:{live}""",500)


			if not text_mode:screen.blit(game_screen,(0,0))
			else:
				data = f"[{closest_pipe[0]},{closest_pipe[1]},\n{birds[cool_bird].bird_top_bottom[0]:.1f},{birds[cool_bird].bird_top_bottom[1]:.1f}]"
				blit_txt(
f"""min:{minimum}
text:{text_mode}
turbo:{turbo_mode}
cool_bird:{cool_bird}
fit:{res[2]}
data:{data}
res:{net.activate(np.array([*closest_pipe,*birds[cool_bird].bird_top_bottom]))[0]:.1f}""",10)
	   
			pygame.display.update()
			
			screen.fill((0,0,0))	
		else:
			print(end=f"{clock.get_fps():.0f}\r")




	generation+=1

def save(something,*path):
	return pickle.dump(something,open(join(*path),'wb'))


def main(file=join("neat_stuff","best.pkl"),max_gens=0):
	config_path = join("neat_stuff", "config-feedforward.txt")
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
