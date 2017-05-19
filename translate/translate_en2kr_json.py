"""
Powered by NAVER API
"""
import os
import sys
import urllib.request
import demjson, json
import re

en_label_file = 'en_imagenet1000.txt'
result_label_file = 'result_imagenet1001.json'

result = open(result_label_file, 'w')

en_label1000 = open(en_label_file, 'r').read()
en_label1000 = demjson.decode(en_label1000)

en_label1001 = []
en_label1001.append('background')

for words in en_label1000:
	en_label1001.append(en_label1000[words])

result_label1001 = {}

url = "https://openapi.naver.com/v1/language/translate"

#client_id, client_secret 
client_ids = []
client_secrets = []

for idx, i in enumerate(en_label1001):
	if idx < int(len(en_label1001)/3):
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
		result_label1001[idx] = {i:kr_w}
	
	elif (idx >= int(len(en_label1001)/3)) and (idx < int(2*len(en_label1001)/3)):
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
		result_label1001[idx] = {i:kr_w}
	
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
		result_label1001[idx] = {i:kr_w}

json.dump(result_label1001, result, ensure_ascii=False)
result.close()
