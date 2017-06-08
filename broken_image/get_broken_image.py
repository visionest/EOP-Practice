from PIL import Image
import os

img_dir = './imgnet_ext'
f = open('broken_image_list.txt', 'w')

broken_image_list = []

def is_broken_image(cand):
	try:
		Image.open(cand)
		return False
	except:
		return True

folder_num = 1

for roots, _, files in os.walk(img_dir):
	print 'processing : ', folder_num
	for file_name in files:
		full_name = roots + '/' + file_name
		if is_broken_image(full_name) == True:
			broken_image_list.append(full_name)
			f.write(full_name + '\n')
	folder_num += 1

print 'broken_image_list' , broken_image_list

f.close()
print 'process complete'
