import serial as serial # interface with arduino
import time # For time.sleep()
import datetime as datetime # To print current date
import serial.tools.list_ports # To look for arduino port
#from urllib.request import urlopen # urlopen for weather
import random as random # to get random fact in history
import requests # To get API request for reminders
import praw # reddit API wrapper


# Search for the arduino serial port
ports = list(serial.tools.list_ports.comports()) # List the serial ports on the computer
for p in ports: # Look through each one
    if("USB" in p[2]): # Look for the word USB which would define the arduino
    	arduinoPort = p[0] # Set the variable arduino port to that address

ser = serial.Serial(arduinoPort, 9600) # Open the serial port on the arduino port address

# Open a new instance of reddit to interface with the reddit API
reddit = praw.Reddit(client_id='b7886IFMbdNIhA',
   	                 client_secret='V3L9CIRkXf6-b9PXyP6Sx0-HKyE',
       	             user_agent='')
reddit.read_only = True # only read reddit posts don't allow editing

try:
	tdih = requests.get('http://history.muffinlabs.com/date') # this day in history api
except:
	pass

# Try to open the reminders API, if not pass since an error will be shown later
try:
	r = requests.get('https://f51852e7.ngrok.io/api/reminders')
except:
	pass

# Print the given string d on the printer, ensuring that every
# word stays within the 32 character width of the printer
def printer(d):
	# define the time to print based on size of string inputted
	timeToPrint = int(float(len(d)) / 32.0)+2 
	currentLength = 0 # current length starts at zero
	totalLength = 0 # total length starts at zero
	final = '' # final used to store output to printer

	# add the finish character to flag the end of the string for the printer
	a = d + '|'
	b = a.decode("utf-8") # decode the input from utf-8
	initial = b.encode("ascii", "ignore") # to encode in ascii which the printer uses

	# cycle through the words in the input
	for word in initial.split():
		currentLength += (len(word)+1)
		totalLength += (len(word)+1)

		if(currentLength < 32):
			final += word + ' '

		elif(currentLength >= 32):
			currentLength -= len(word)+1
			totalLength -= len(word)+1
			while(currentLength != 31):
				final += ' '
				currentLength += 1
				totalLength += 1
			final += word + ' '
			currentLength = len(word)
			totalLength += len(word)


	totalLength -= 4

	ser.write(final)
	time.sleep(timeToPrint)

def printerFeed():
	# Feeds blank paper to the printer at the end of the print job
	printer('')

def printerBreak():
	# adds a broken line between sections
	printer('-------------------------------')


# print the current date at top of page and last update time
def header():
	printer("Today is " + datetime.date.today().strftime("%B %d, %Y") + ' updated at ' + datetime.datetime.today().strftime("%H:%M")) # show the current date
	printerBreak()

# Show the morning news pulled from the top posts of r/news and r/worldnews
def morningNews():
	printer("Todays top stories from r/worldnews and r/news:") # header for news

	# try to access r/news
	try:
		# cycle through the top 5 posts
		for submission in reddit.subreddit('worldnews+news').hot(limit=6):
			strtitle = str((submission.title).encode('utf-8')) # grab title
			printer(strtitle) # print headline/title of each

	# if reddit could not be reached throw error about network
	except:
		printer("reddit could not be reached, please check your connection")

	printerBreak()

# Show reminders from the reminders API
def getReminders():
	printer("On your to-do list:") # print header
	try:
		for i in r.json(): # cycle through reminders in json file returned by API
			printer(i['text'] + ' due on ' + i['date_reminder']) # print reminder text for each
	# if the server could not be reached, show an error
	except:
		printer("Your reminders could not be found at this time")
	printerBreak()

# Show a daily joke from top of r/jokes
def dailyJoke():
	printer("Your daily joke:") # Print header
	# grab top post from r/jokes
	try:
		for submission in reddit.subreddit('jokes').hot(limit=1):
			printer(submission.title) # print title of joke
			printer(submission.selftext) # print body of joke
	except:
		printer('Reddit could not be reached please check your connection')
	printerBreak()

# Show this day in history fact
def thisDayInHistory():
	# Define three random indeces in the range of the json file
	try:
		i = random.randint(0, (len(tdih.json()['data']['Events'])-1))
		j = random.randint(0, (len(tdih.json()['data']['Events'])-1))
		k = random.randint(0, (len(tdih.json()['data']['Events'])-1))

		#ensure that the indeces are not the same to get three distinct events
		while(i == j):
			j = random.randint(0, (len(tdih.json()['data']['Events'])-1))
		while(j == k):
			k = random.randint(0, (len(tdih.json()['data']['Events'])-1))

		# grab the three years from the json file
		year1 = int(tdih.json()['data']['Events'][i]['year'])
		year2 = int(tdih.json()['data']['Events'][j]['year'])
		year3 = int(tdih.json()['data']['Events'][k]['year'])

		# grab the raw text of the event from the json
		text1a = (tdih.json()['data']['Events'][i]['text'])
		text2a = (tdih.json()['data']['Events'][j]['text'])
		text3a = (tdih.json()['data']['Events'][k]['text'])

		# decode the text from utf-8
		text1b = text1a.decode("utf-8")
		text2b = text1a.decode("utf-8")
		text3b = text1a.decode("utf-8")

		# encode in ascii and ignore errors to be able to pass to printer
		text1 = text1b.encode("ascii", "ignore")
		text2 = text2b.encode("ascii", "ignore")
		text3 = text3b.encode("ascii", "ignore")

		# formulate three responses from the year and text of event
		response1 = 'In ' + str(year1) + ' ' + str(text1)
		response2 = 'In ' + str(year2) + ' ' + str(text2)
		response3 = 'In ' + str(year3) + ' ' + str(text3)

		printer('This day in history: ') # Heading for this section
		printer(response1) # Print the three responses
		printer(response2)
		printer(response3)
	except:
		printer("Today's history will be rembered without internet")

	printerBreak() # create the break line at the bottom of this section


def getWeather():
	# get the json file for the weather forecast
	f = requests.get('http://api.wunderground.com/api/62cf407a8229ef86/geolookup/forecast/q/MA/Boston.json')
	
	# parse out the forecast for today and for tomorrow
	forecast = f.json()['forecast']['txt_forecast']['forecastday'][0]['fcttext']
	tomorrow = f.json()['forecast']['txt_forecast']['forecastday'][2]['fcttext']

	# print out the respective forecasts
	printer('Weather forecast in Boston: ' + str(forecast))
	printer('Weather tomorrow in Boston: ' + str(tomorrow))
	printerBreak() # print break line

#header()
#morningNews()
#getWeather()
#getReminders()
#dailyJoke()
#thisDayInHistory()


printerFeed()