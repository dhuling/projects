import requests


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
		
def AlbumCheck(url1):
	if url1[17] == 'a':
		print "This is part of an album"
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
	if not_saved < 9:
		print "\n"
		print "Images NOT saved"
		print "---------------------"
		print "|                   |"
		print "|         %d        |" % not_saved
		print "|                   |"
		print "---------------------"
	else:
		print "\n"
		print "Images NOT saved"
		print "---------------------"
		print "|                   |"
		print "|         %d       |" % not_saved
		print "|                   |"
		print "---------------------"