
#----------IMPORTS-----------------
# mods2 contains the majority of the logic.
import imp
import mods2 as m
import sys

#import requests


#this module was included to time the program. its a bit useless because 
# i ask for user input, which doesn't really time the process anyway


# ---------- Main ------------
# Using the requests module, get the json objects from whichever subreddit.
# TODO: ask user for subreddit, create query for them and run it as a loop,
# 	so they can get from as many subs as they like

# retrieves the json objects to be parsed
try:
	import requests
	r = requests.get("http://www.reddit.com/r/wallpapers/top/.json?sort=top&t=day&limit=50")
	f = requests.get("http://www.reddit.com/r/earthporn/top/.json?sort=top&t=day&limit=50")

# Core logic is done by GetImages, which is a chain of processes in the mods2
# module. GetImages executes image saving, error handling, and file checking
# by using functions contained within mods2
# imgsave == how many images were saved, nosave == how many were not saved
# j is a list of the images that were not saved, which can then be passed
# to WebReturn function in order to view them manually, if wished.
	imgsave, nosave, j = m.GetImages(r)
	imgsave1, nosave1, j = m.GetImages(f)

# total saved and not saved
	saved = imgsave + imgsave1
	not_saved = nosave + nosave1

# DrawResults gives us a pretty textual output. could try to make a simple
# gui with ttk later

	m.DrawResults(saved, not_saved)

# This conditional asks user if they want to view the unsaved pictures
# Usually the problem is people locking down their flikr account. 
# TODO: perhaps make a flicker crawler to download (like the deviantart)

	if len(j) > 0:
		print "There are ", not_saved , "Unsaved results."
		s = raw_input( "Would you like to view unsaved images? Y or N \n>>> ")
		if s == 'y' or s == 'Y':
			w = int(raw_input( "Returned Unsave Limit?\n>>>" ))
			m.WebReturn(j, w)
		else:
			pass

# This loop keeps the terminal open, allowing the user to view
# the results of the scrape.
	quit = False
	while quit == False:
		input = raw_input("Do you want to quit? Y or N: ")
		if input == 'y' or input == 'Y':
			quit = True
			continue
			quit()
		else:
			continue 
except ImportError as e:
	print e
	raise
	input ("HOOOOPLAY")