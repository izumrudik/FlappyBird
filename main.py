import os
import argparse
import sys
def resource_path(*relative):
	relative = os.path.join(*relative)
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative)
	return os.path.join(relative)

def main():
	parser = argparse.ArgumentParser(description="""A flappy bird game!\n
You can use -t flag to run training (try pressing "p","t" and "m" )\n
You can use -l flag to run best genome\n
You can use -p flag to play yourself  (try pressing "m" )""")


	group = parser.add_mutually_exclusive_group()
	group.add_argument("-t","--train"  ,action="store_true",help="used to make trained bird's file (-f) with maximum (-g) generations")
	group.add_argument("-l","--learned",action="store_true",help="used to run learned bird's simulation from file (-f)")
	group.add_argument("-p","--play", action="store_true",help="used to run game in singleplayer")
	parser.add_argument("-f","--file",type=str,default=resource_path("neat_stuff","best.pkl"),help="file name",metavar="")
	parser.add_argument("-g","--generations",type=int,default=10,help="int number of generations ",metavar="")


	args = parser.parse_args()



	from game import main as run_game_for_one_user
	from train import main as train_main
	from work import main as work_main

	if args.learned:
		work_main(args.file)
	if args.train:
		train_main(args.file,args.generations)
	else:
		run_game_for_one_user()






if __name__ == "__main__":
	main()
