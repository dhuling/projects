import requests
import json
import urllib
import urllib2
import csv
from mods import ImgrCheck, DrawResults, AlbumCheck

def getContentType(pageUrl):
	try:
		page = urllib2.urlopen(pageUrl)
		pageHeaders = page.headers
		contentType = pageHeaders.getheader('content-type')
		return contentType
	except:
		print "CANNOT OPEN URL, IMAGE NOT SAVED"
		return 'bool'

r = requests.get('http://www.reddit.com/r/mapporn/top/.json?sort=top&t=day&limit=30')
r.text
data = r.json()
iter_len = len(data['data']['children'])
imgsave = 0
nosave = 0

#Opens the file for reading to check dups
with open('archive.csv', 'rb') as archive:
	reader = csv.reader(archive)
	with open('archive.csv', 'a+') as arc:	
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
			print "Url: " + "\n" + "-----" + url
			ext = getContentType(url)
			isDuplicate = False
			#Check for dups
			for row in reader:
				q = str(row)
				if webp in q:
					print "Duplicate!"
					isDuplicate = True
					nosave += 1
					continue
					
			if isDuplicate == False or 'bool' in ext:
			#checks filetype. Will only save jpegs and pngs, not full webpages or other image types
				if "jpeg" in ext:
					try:
						urllib.urlretrieve(url, name + ".jpg")
						print "Image Saved"
						imgsave += 1
					except:
						print "Web Error"
						nosave += 1
						continue
				elif "png" in ext:
					try:
						urllib.urlretrieve(url, name + ".png")
						print "Image Saved"
						imgsave += 1
					except:
						print "Web Error"
						nosave += 1
						continue
				elif ImgrCheck(domain, ext, url) == True:
					url2 = url + ".jpg"
					try:
						urllib.urlretrieve(url2, name + ".jpg")
						print "Image Saved"
						imgsave += 1
					except:
						print "Web Error"
						nosave += 1
						continue
				
				else:
					print "THIS IS NOT A SUPPORTED TYPE, NOT SAVED"
					print AlbumCheck(url)
					print "EXT" , ext
					nosave += 1
					continue
				
				arcwriter = csv.writer(arc, delimiter=' ')
				arcwriter.writerow( [url] )
			if isDuplicate == True:
				print "This is a duplicate image, not saving"
			
results = DrawResults(imgsave, nosave)

quit = False
while quit == False:
	input = raw_input("Do you want to quit? Y or N: ")
	if input == 'y' or input == 'Y':
		quit = True
		continue
	else:
		continue 
		