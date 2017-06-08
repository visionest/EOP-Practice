import os
from subprocess import call

NUMBER = 1000

extractlist = []
with open('removed_choice1000.txt') as f:
	for line in f:
		line = line.strip()
		extractlist.append(line)
assert NUMBER == len(extractlist), "length not same"

cnt = 0

print "list finish"
for filename in extractlist:
	foldername = filename.replace('.tar','')
	call(['tar', '-xf', './imgnet_small/'+filename, '-C', './imgnet_ext/'+foldername])
	cnt += 1
	print 'count = ', cnt

print "extract finish"
