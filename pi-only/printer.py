'''
This program is to be run in Python2 to interface with an Adafruit
Thermal receipt printer.  Multiple arguments are provided to change
the font styling according to the Adafruit documentation.

Call this program in python3 as follows:
subprocess.Popen("python2 printer.py "Text to print".split())

Add any flags or arguments as necessary:
Bold -b
Underline -u
Inverse -i
Tall -t
Large - l
Medium - m
Small -s

To feed after print, use the -f flag with number of lines following
Example: "-f 4" for four lines fed after print.


'''

import argparse
import Adafruit_Thermal as adf

printer = adf.Adafruit_Thermal('/dev/serial0', 19200, timeout=5)

# Initilaize the Argument parser
parser = argparse.ArgumentParser(description="Wrapper for Adafruit Thermal in Python3")
parser.add_argument('to_print') # Add argument for text to be printed

# Add arguments for optional settings
parser.add_argument('--large', '-l', action='store_true')
parser.add_argument('--medium', '-m', action='store_true')
parser.add_argument('--small', '-s', action='store_true')
parser.add_argument('--bold', '-b', action='store_true')
parser.add_argument('--inverse', '-i', action='store_true')
parser.add_argument('--tall', '-t', action='store_true')
parser.add_argument('--underline', '-u', action='store_true')
parser.add_argument('--feed', '-f', nargs=1)
parser.add_argument('--justify', '-j')

# Parse the arguments
args = parser.parse_args()
if(not args.feed): args.feed = 3
else: args.feed = int(args.feed[0])

# Check font styling
if(args.bold):
	printer.boldOn()
if(args.inverse):
	printer.inverseOn()
if(args.tall):
	printer.doubleHeightOn()
if(args.underline):
	printer.underlineOn()

# Check size of text
line_length = 32 # Set the default characters per line
if(sum([args.large, args.medium, args.small]) > 1):
	raise ValueError("Too many sizes selected")
else:
	if(args.large):
		printer.setSize('L')
		line_length = 16
	elif(args.medium):
		printer.setSize('M')
		line_length = 32
	elif(args.small):
		printer.setSize('S')
		line_length = 32

# Check justification
if(args.justify):
	if(args.justify.lower() == 'l' or args.justify.lower() == 'left'):
		printer.justify('L')
	elif(args.justify.lower() == 'r' or args.justify.lower() == 'right'):
		printer.justify('R')
	elif(args.justify.lower() == 'c' or args.justify.lower() == 'center'):
		printer.justify('C')
	else:
		raise ValueError("Invalid justification option: " + str(args.justify))

# Print the results
# Cut the rows so the text wraps
# None of the text formatting changes width, just text size
print("Parsed: " + str(args))
print("Printing: " + str(args.to_print))
print("Feed: " + str(args.feed) + ", type: " + str(type(args.feed)))

printer.println(args.to_print)
printer.feed(args.feed)

# Return to default settings
printer.setDefault()
