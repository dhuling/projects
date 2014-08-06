import os

#this code is implemented to automatically create directories
incident = raw_input("Please input the name of the disaster (keep it short): ")
spatial = ["Country", "Region", "Prefecture", "City", "Ward"]
indicators = ["Economic", "Transportation", "Communications", 
              "Electricity", "Water", "Demographics", "Health and Human Services",
			  "Education", "Government and Planning", "Housing Recovery"]
folder = os.getcwd() + "/"
os.mkdir(os.path.expanduser(folder + incident))		  
for i in indicators:
	os.mkdir(os.path.expanduser(folder + "\\" + incident + "\\" + i))

