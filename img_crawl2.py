# -*- coding: utf-8 -*-
# @Author: Rui

from multiprocessing import Pool
import time
import urllib
import itertools
import requests
import re
import os
import sys
# import myglobal
import random

# Special string table
str_table = {
	'_z2C$q': ':',
	'_z&e3B': '.',
	'AzdH3F': '/'
}

# Character translate table
# Use maketrans() to create a translation map
intab = b"abcdefghijklmnopqrstuvw1234567890"
outab = b"0852vsnkheb963wtqplifcadgjmoru147"
char_table = bytes.maketrans(intab, outab)

# Decode the urls
def decode(url):
	for key, value in str_table.items():
		# Replace str_table items
		url = url.replace(key, value)
	# Replace char_table items
	return url.translate(char_table)

# Generate url list automatically
# generator
def generateUrls(word):
	world = urllib.parse.quote(word)
	url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={word}&z=&ic=0&face=0&istype=2&qc=&nc=1&fr=&step_word={word}&pn={pn}&rn=30"
	urls = (url.format(word = word, pn = x) for x in range())
	return urls

def makeDir(dirName):
	dirPath = os.path.join(sys.path[0], dirName)
	if not os.path.exists(dirPath):
		os.mkdir(dirPath)
	return dirPath

reg = re.compile(r'"objURL":"(.*?)"')


def downloadImgProcess(url, dirPath):
	print("Now process %s running..." % os.getpid())
	html = requests.get(url, timeout = 10).content.decode('utf-8')
	imgUrls = [decode(x) for x in re.findall(reg, html)]
	if len(imgUrls) == 0:
		return 
	for imgUrl in imgUrls:
		filename = os.path.join(dirPath, str(random.random()) + '.jpg')
		try:
			res = requests.get(imgUrl, timeout = 15)
			if str(res.status_code)[0] == '4':
				print(str(res.status_code), ':', imgUrl)
				continue
		except Exception as e:
			print('Exception: ', imgUrl)
			print(e)
			continue
		with open(filename, 'wb') as f:
			f.write(res.content)
			# print('Downloading imgs %s...' % myglobal.index)
			# myglobal.index += 1		
	return	

def main():
	print("IAMGE CRAWLER")
	print("This script can help you download images automatically from Baidu")
	print("******************************************************************")
	# Get key_word
	word = input("Please input the key_word for downloading images: \n")
	# make a new file for saving images
	dirPath = makeDir(word)
	
	p = Pool(40)
 	
	print("Now process %s running..." % os.getpid())
	# Get urls generated automatically
	urls = generateUrls(word)
	# Get start time
	start = time.time()
	p.map(downloadImgProcess, urls)

	p.close()
	p.join()
	end = time.time()
	print('All subprocesses done.')
	# print('Totally download %d images.' % (myglobal.index-1))
	print('Totally use %.2f seconds.' % (end-start))


if __name__ == '__main__':
	main()