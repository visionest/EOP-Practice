import os
from subprocess import call

NUMBER = 1000

extractlist = []
with open('removed_choice1000.txt') as f:
	for line in f:
		line = line.strip()
		extractlist.append(line)
assert NUMBER == len(extractlist), "length not same"

print "list finish"
for filename in extractlist:
	call(['tar', '-xvf', 'fall11_whole.tar', filename])
	call(["mv", filename, "./imgnet_small"])
print "extract finish"
