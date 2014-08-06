import requests
from bs4 import BeautifulSoup as bs
import urllib

#get source code to parse
r = requests.get("http://www.co.pacific.wa.us/gis/DesktopGIS/WEB/index.html")
html = r.text

#parse through to get links to files
soup = bs(html)

#link containers
h, j = [], []

#gets all the links
for link in soup.find_all("a"):
	h.append(link.get("href"))
#narrows to just zip files (shpfiles)
for i in h:
	if "zip" in i:
		j.append(i)
	
url ="http://www.co.pacific.wa.us/gis/DesktopGIS/WEB/"

for i in j:
	print "Saving " + url + i
	urllib.urlretrieve(url+i, "C:/Users/Derek/Documents/WWU/Thesis/PacCountyGIS/" + i[0:len(i)-4] + ".zip")
	print "Success"
