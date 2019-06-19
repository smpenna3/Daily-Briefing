## Python3 only!

import serial as serial
import requests
import json
import time


# Printer will print 32 wide
def printer(d):
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	time.sleep(2)
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

	ser.write(final.encode())
	time.sleep(timeToPrint)
	print(final)
	print(final.encode())

if __name__ == '__main__':
	d = ''

	while(d != 'exit'):
		a = input('print: ')
		printer(a+'|')
