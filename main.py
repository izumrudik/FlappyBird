from game import main as run_game_for_one_user
from train import main as train_main
from work import main as work_main
import os
import argparse
parser = argparse.ArgumentParser(description="A flappy bird game!")


def main():
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-t","--train"  ,action="store_true",help="used to make trained file")
	group.add_argument("-l","--learned",action="store_true",help="used to run learned bird's simulation from file")
	group.add_argument("-p","--play", action="store_true",help="used to run game in singleplayer")
	parser.add_argument("-f","--file",type=str,default=os.path.join("neat_stuff","best.pkl"))
	parser.add_argument("-P","--populations",type=int,default=10)



	args = parser.parse_args()

	if args.learned:
		work_main(args.file)
	if args.train:
		train_main(args.file,args.populations)
	else:
		run_game_for_one_user()






if __name__ == "__main__":
	main()