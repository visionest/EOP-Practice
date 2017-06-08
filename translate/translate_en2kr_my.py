"""
Powered by NAVER API
"""
import os
import sys
import urllib.request
import json
import re

# My label as synset
synset_file = 'my_synsets.txt'
# Whole label with synset
whole_file = 'words.txt'
result_file = 'result_my1000.json'

result = open(result_file,'w')
synset = open(synset_file, 'r')
whole = open(whole_file, 'r')

MY_CLASSES = 1000
WHOLE_CLASSES = 82115

s_dict = {}
s_list = []

w_dict = {}
en_label = []

# My synset load
for sline in synset:
	sline = sline.strip()
	s_list.append(sline)
assert MY_CLASSES == len(s_list), 'number of class does not match!'

# Whole en_label with synset load
for wline in whole:
	wline = wline.split('\t')
	wd = wline[-1].strip()
	w_dict[wline[0]] = wd
assert WHOLE_CLASSES == len(w_dict), 'number of whole words does not match!!'

# My synset with en_label
for sidx, s in enumerate(s_list):
	s_dict[sidx] = w_dict[s]
assert MY_CLASSES == len(s_dict), 'number of class with idx does not match!!!'

# My en_label
for lidx in s_dict:
	en_label.append(s_dict[lidx])
assert MY_CLASSES == len(en_label), 'number of class with label does not match!!!!'

# Result {'class_num' : {'en_label' : 'kr_label'} , ... }
kr_label1000 = {}

url = "https://openapi.naver.com/v1/language/translate"

#client_ids, client_secrets
client_ids = []
client_secrets = []

print ('main process start')
for idx, i in enumerate(en_label):
	if idx < int(len(en_label)/3):
		i_sp = re.split(',', i)
		tmp = []
		for word in i_sp:
			word = word.lstrip().rstrip()
			encText = urllib.parse.quote(word)
			data = "source=en&target=ko&text=" + encText

			request = urllib.request.Request(url)
			request.add_header("X-Naver-Client-Id",client_ids[0])
			request.add_header("X-Naver-Client-Secret",client_secrets[0])
			response = urllib.request.urlopen(request, data=data.encode("utf-8"))
			rescode = response.getcode()

			if(rescode==200):
				response_body = response.read()
				res_json = json.loads(response_body.decode('utf-8'))
				tmp.append(res_json['message']['result']['translatedText'])
			else:
				print("Error Code:" + rescode)

		kr_w = ','.join(tmp)
		kr_label1000[idx] = {i:kr_w}

	elif (idx >= int(len(en_label)/3)) and (idx < int(2*len(en_label)/3)):
		i_sp = re.split(',', i)
		tmp = []
		for word in i_sp:
			word = word.lstrip().rstrip()
			encText = urllib.parse.quote(word)
			data = "source=en&target=ko&text=" + encText

			request = urllib.request.Request(url)
			request.add_header("X-Naver-Client-Id",client_ids[1])
			request.add_header("X-Naver-Client-Secret",client_secrets[1])
			response = urllib.request.urlopen(request, data=data.encode("utf-8"))
			rescode = response.getcode()

			if(rescode==200):
				response_body = response.read()
				res_json = json.loads(response_body.decode('utf-8'))
				tmp.append(res_json['message']['result']['translatedText'])
			else:
				print("Error Code:" + rescode)

		kr_w = ','.join(tmp)
		kr_label1000[idx] = {i:kr_w}

	else:
		i_sp = re.split(',', i)
		tmp = []
		for word in i_sp:
			word = word.lstrip().rstrip()
			encText = urllib.parse.quote(word)
			data = "source=en&target=ko&text=" + encText

			request = urllib.request.Request(url)
			request.add_header("X-Naver-Client-Id",client_ids[2])
			request.add_header("X-Naver-Client-Secret",client_secrets[2])
			response = urllib.request.urlopen(request, data=data.encode("utf-8"))
			rescode = response.getcode()

			if(rescode==200):
				response_body = response.read()
				res_json = json.loads(response_body.decode('utf-8'))
				tmp.append(res_json['message']['result']['translatedText'])
			else:
				print("Error Code:" + rescode)

		kr_w = ','.join(tmp)
		kr_label1000[idx] = {i:kr_w}

json.dump(kr_label1000, result, ensure_ascii=False)
result.close()
print ('Check length of dictionary :', len(kr_label1000))
print ('process complete!!')
