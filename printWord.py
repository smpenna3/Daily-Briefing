import serial as serial
import requests
import json
import time


# Printer will print 32 wide
def printer(d):
	ser = serial.Serial('/dev/ttyACM0', 9600)
	timeToPrint = int(float(len(d)) / 32.0)+3
	currentLength = 0
	totalLength = 0
	final = ''

	for word in d.split():
		currentLength += (len(word)+1)
		totalLength += (len(word)+1)
		#print(word + '  current length ' + str(currentLength))

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

d = ''

while(d != 'exit'):
	a = raw_input('print: ')
	b = a + '|'

	c = b.decode("utf-8")
	d = c.encode("ascii", "ignore")

	printer(d)