#!/usr/bin/python

# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
import sys
import telegram_send

argv = sys.argv

# settings
# nameVerhuurder = 'Rochdale'
# checkURL = 'https://www.rochdale.nl/aanbod/vrijesector'
# checkTimer = 30
# goToURL = 'https://www.rochdale.nl/aanbod/vrijesector'

nameVerhuurder = argv[1]
checkURL = argv[2]
goToURL = argv[3]
checkTimer = int(argv[4])

# ##########################

# setting the URL you want to monitor
url = Request(checkURL,
			headers={'User-Agent': 'Mozilla/5.0'})

# to perform a GET request and load the
# content of the website and store it in a var
response = urlopen(url).read()

# to create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
print('huizenchecker for: ' + str(argv))
print(nameVerhuurder + " watcher running...")
telegram_send.send(messages=[nameVerhuurder + " watcher is now running!"])

time.sleep(2)
while True:
	try:
		# perform the get request and store it in a var
		response = urlopen(url).read()
		
		# create a hash
		currentHash = hashlib.sha224(response).hexdigest()
		
		# wait for 30 seconds
		time.sleep(checkTimer)
		
		# perform the get request
		response = urlopen(url).read()
		
		# create a new hash
		newHash = hashlib.sha224(response).hexdigest()

		# check if new hash is same as the previous hash
		if newHash == currentHash:
			continue

		# if something changed in the hashes
		else:
			# notify
			print("NIEUWE " + nameVerhuurder + " LISTING!")
			telegram_send.send(messages=["New " + nameVerhuurder + " listing- open: " + goToURL])

			# again read the website
			response = urlopen(url).read()

			# create a hash
			currentHash = hashlib.sha224(response).hexdigest()

			# wait for 30 seconds
			time.sleep(checkTimer)
			continue
			
	# To handle exceptions
	except Exception as e:
		print("error:")
		print(e)