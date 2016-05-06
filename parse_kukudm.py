from bs4 import BeautifulSoup
import requests
import sys
import re
import webbrowser

def store_imgurl_to_list(comicpage, imgurl_list):
	'''
	Take a url as an argument, this function will store the image url link on that page to a list.
	The first argument is the url, second argument is the variable name that result will store in.
	'''
	#retrieve the javascript into string variable "target"
	r = requests.get(comicpage)
	soup = BeautifulSoup(r.content ,'html.parser')
	target = str((soup.find_all('script',{'language':'javascript'})[2]))
	#get imgurl through regex from "target"
	imgurl = re.findall(r'\"(.+?)\"',target)
	# imgurl is now ['<img id=comicpic name=comicpic src=','kuku3comic3/yh/vol_03/kuku_0124LS.jpg\'>']
	del imgurl[0]
	imgurl = imgurl[0] + 'http://n.kukudm.com/' + imgurl[1]
	imgurl_list.append(imgurl)


def write_html(list,file):
	'''
	write the list into the file
	'''
	#append into html page
	#produce a clean html file with all the picture
	with open('pics/pics.html', 'w', encoding='utf-8') as file:
	    file.write('')

	with open('pics/pics.html', 'a', encoding='utf-8') as file:
	    for imgurl in imgurl_list:
	        file.write( imgurl +'<br>')

def url_extracting(anyurl):
	'''
	Give the first page url of the comic book, this function will return all the page url in a list.
	'''
	#retrieve the javascript into string variable "target"
	r = requests.get(anyurl)
	soup = BeautifulSoup(r.content ,'html.parser')
	target = str(soup)
	#get imgurl through regex from "target"
	page_numbers = int(re.findall(r'\共(.+?)\页',target)[0])
	url_list = []
	for i in range(1,page_numbers+1):
		url = anyurl.replace('1.htm', str(i)+'.htm' )
		url_list.append(url)
	return (url_list)


imgurl_list = []
comicbook = input('''give me first page url of that comic book: 
for example \'http://comic.kukudm.com/comiclist/364/5048/1.htm\'
Please note that only comics on http://comic.kukudm.com/ will be available
And that the process may continue for 2 to 3 minutes  
 ''') 
url_list = url_extracting(comicbook)
for url in url_list:
	store_imgurl_to_list(url, imgurl_list)
write_html(imgurl_list,'pics/pics.html')

webbrowser.open('file:///C:/Users/tj371_000/Desktop/venv_parse/src/pics/pics.html')

