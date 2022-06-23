#!/usr/bin/python

# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
import sys
import telegram_send
import requests
import os
from bs4 import BeautifulSoup

argv = sys.argv

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

def process_html(string):
    soup = BeautifulSoup(string, features="html5lib")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select('script'):
        s.extract()

    # remove meta tags 
    for s in soup.select('meta'):
        s.extract()
    
    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')

def webpage_was_changed(): 
    """Returns true if the webpage was changed, otherwise false."""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(checkURL, headers=headers)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists('previous_content_' + nameVerhuurder + '.txt'):
        open('previous_content_' + nameVerhuurder + '.txt', 'w+').close()
    
    filehandle = open('previous_content_' + nameVerhuurder + '.txt', 'r')
    previous_response_html = filehandle.read() 
    filehandle.close()

    processed_response_html = process_html(response.text)

    if processed_response_html == previous_response_html:
        return False
    else:
        filehandle = open('previous_content_' + nameVerhuurder + '.txt', 'w')
        filehandle.write(processed_response_html)
        filehandle.close()
        return True

time.sleep(2)

while True:
	if webpage_was_changed():
		print("NIEUWE " + nameVerhuurder + " LISTING!")
		telegram_send.send(messages=["New " + nameVerhuurder + " listing- open: " + goToURL])
	time.sleep(checkTimer)

# while True:
# 	try:
# 		# perform the get request and store it in a var
# 		response = urlopen(url).read()
		
# 		# create a hash
# 		currentHash = hashlib.sha224(response).hexdigest()
		
# 		# wait for 30 seconds
# 		time.sleep(checkTimer)
		
# 		# perform the get request
# 		response = urlopen(url).read()
		
# 		# create a new hash
# 		newHash = hashlib.sha224(response).hexdigest()

# 		# check if new hash is same as the previous hash
# 		if newHash == currentHash:
# 			continue

# 		# if something changed in the hashes
# 		else:
# 			# notify
# 			print("NIEUWE " + nameVerhuurder + " LISTING!")
# 			telegram_send.send(messages=["New " + nameVerhuurder + " listing- open: " + goToURL])

# 			# again read the website
# 			response = urlopen(url).read()

# 			# create a hash
# 			currentHash = hashlib.sha224(response).hexdigest()

# 			# wait for 30 seconds
# 			time.sleep(checkTimer)
# 			continue
			
# 	# To handle exceptions
# 	except Exception as e:
# 		print("error:")
# 		print(e)
