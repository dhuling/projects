import requests
import json
import urllib
import urllib2
import csv
import webbrowser as w
try:
	from bs4 import BeautifulSoup
except:
	from beautifulsoup4 import BeautifulSoup
from pprint import pprint
import sys
import time

def AlbumDownL(url):
	a = Save_Links(url)
	return a
def getSource(url1):
	r = requests.get(url1)
	html = r.text
	html1 = html.encode("ascii", "ignore")
	return html

def Get_Album_Links(url1):
	"""Depends on getSource"""
	source = getSource(url1)
	soup = BeautifulSoup(source)
	#need the ResultSet object to be a string
	result = str(soup.find_all("div", class_ = "options"))
	
	#soupifying the result set to return more 
	soup2 = BeautifulSoup(result)
	#h will contain all links, j will contain links we'll use
	h, j = [], []
	
	#Get all a tags out of the narrowed search
	for link in soup2.find_all("a"):
		h.append(link.get("href"))
	
	
	#Get all links we're going to use from h
	for i in range( 0, len(h), 2):
		j.append(h[i])
	
	return j

#This is the control function for downloading albums. This needs to be called
def Save_Links(url2):
	"""depends on Get_Album_Links"""
	links = Get_Album_Links(url2)
	out = str(len(links))
	sys.stdout.write("\nSaving an additional " + out + " in album images\n")
	num = 0
	for i in links:
		r = str(i)
		name = r[14:21]
		url0 = "http:" + r
		r = urllib.urlretrieve(url0, name + ".jpg")
		sys.stdout.write(str(num+1) + "/" + out + "... Album Image Saved\n")
		num += 1
	return num
def UserInput():
	subred = raw_input("Subreddit? Spelling matters: ")
	times = raw_input("day, week, month, year? ")
	numres = raw_input("how many results do you want? Max 100:" )
	conurl = "http://www.reddit.com/r/" + subred + "/top/.json?sort=top&t=" + times + "&limit=" + numres
	print "Pulling Content from: \n" + conurl
	return conurl

def CheckType(url):
	try:
		s = requests.get(url)
		ext = s.headers.get('content-type')
		return ext
	except:
		return "bool"
		
def ImgrCheck(domain, ext, url1):
	if 'imgur' in domain and 'text' in ext and AlbumCheck(url1) == False:
		return True
	else:
		return False

def DevCheck(domain):
	if 'deviant' in domain:
		return True
	else:
		return False
		
def DevArt(url1):
	url = url1
	r = getSource(url)
	soup = BeautifulSoup(r)
	soup = soup.find_all("meta", attrs={"name":"og:image"})
	soup = str(soup)
	
	soupy = BeautifulSoup(soup[0:200])
	
	tag = soupy.meta
	
	link = tag['content']
	
	return str(link)
		
def AlbumCheck(url1):
	
	if url1[-8:-5] == '/a/':
		return True
	else:
		return False
		
def DrawResults(saved, not_saved):
	print "\n"
	print "Images Saved"
	print "---------------------"
	print "|                   |"
	print "|         %d        |" % saved
	print "|                   |"
	print "---------------------"
	print "\n"
	print "Images NOT saved"
	print "---------------------"
	print "|                   |"
	print "|         %d        |" % not_saved
	print "|                   |"
	print "---------------------"

def GetImages(r):
	r.text
	data = r.json()
	iter_len = len(data['data']['children'])
	imgsave = 0
	nosave = 0
	savez, nosavez = 0, 0
	j = []
	sys.stdout.write("Saving " + str(iter_len) + " files\n")
	#loop runs the length of the query
	for i in range(iter_len):
		#parsing json dicts 
		url = data['data']['children'][i]['data']['url']
		name = data['data']['children'][i]['data']['id']
		title = data['data']['children'][i]['data']['title']
		domain = data['data']['children'][i]['data']['domain']
		#getting length of list to extract string
		urllen = len(url)
		#webp is a string form of the list url
		webp = str(url[0:urllen])
		output = str(i+1) + "/" + str(iter_len)
		sys.stdout.write(output)
		ext = CheckType(url)
		isDuplicate = False
		with open('archive.csv', 'rb') as arc:
			reader = csv.reader(arc)
			for row in reader:
				q = str(row)
				if webp in q:
					
					isDuplicate = True
					nosave += 1
					sys.stdout.write(" .... Duplicate\n")
					continue
				
		#debug check print isDuplicate
		if isDuplicate == False:
		#checks filetype. Will only save jpegs, pngs, gifs, not full webpages or other image types
			if "jpeg" in ext:
				try:
					urllib.urlretrieve(url, name + ".jpg")
					
					imgsave += 1
				except:
					sys.stdout.write(" .... jpeg Error, not saved\n")
					nosave += 1
					continue
			elif "png" in ext:
				try:
					urllib.urlretrieve(url, name + ".png")
					
					imgsave += 1
				except:
					sys.stdout.write(" .... png Error, not saved\n")
					nosave += 1
					continue
			elif "gif" in ext:
				try:
					urllib.urlretrieve(url, name + ".gif")
					print "Image Saved"
					imgsave += 1
				except:
					sys.stdout.write(" .... gif Error, not saved\n")
					nosave += 1
					continue
			elif ImgrCheck(domain, ext, url) == True:
				url2 = url + ".jpg"
				try:
					urllib.urlretrieve(url2, name + ".jpg")
					
					imgsave += 1
				except:
					sys.stdout.write(" .... Imgur Error, not saved\n")
					nosave += 1
					continue
			elif AlbumCheck(url):
				savez = AlbumDownL(url)
			elif DevCheck(domain):
				dev = DevArt(url)
				try:
					urllib.urlretrieve(dev, name + ".jpg")
					
					imgsave += 1
				except:
					sys.stdout.write(" .... Dev Art Error, not saved\n")
					nosave += 1
					continue
					
			else:
				sys.stdout.write(" .... Error, not saved       Site: " + domain + "\n")
				nosave += 1
				j.append(str(url))
				continue
			
			with open('archive.csv', 'a+') as arc:
				arcwriter = csv.writer(arc, delimiter=' ')
				arcwriter.writerow( [url] )
				
			sys.stdout.write(" . . . . Saved\n")
		if isDuplicate == True:
			pass
	save = [imgsave+savez, nosave, j]
	return save	

def getContentType(pageUrl):
	try:
		page = urllib2.urlopen(pageUrl)
		pageHeaders = page.headers
		contentType = pageHeaders.getheader('content-type')
		return contentType
	except:
		return 'bool'	
		
def WebReturn(j, a):
	"""Send WebReturn a list of websites to be opened"""
	i = 0
	for item in j:
		if i < a:
			w.open_new_tab(item)
		else:
			break
		i += 1
	
def ModsVers():
	print "THIS IS MODS V2"
	
def PrintSlow(l):
	for i in l:
		sys.stdout.write(i)
		time.sleep(0.07)
	print ""