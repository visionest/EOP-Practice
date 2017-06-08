import re
NUM_CLASSES = 1000

res = open('imagenet_my_synsets.txt', 'w')

with open('removed_choice1000.txt') as f:
	for line in f:
		line = line.strip()
		line = line.replace('.tar', '')
		res.write(line+'\n')

res.close()
