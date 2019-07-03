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
parser.add_argument('--test', action='store_true') # Test and don't print
parser.add_argument('--feed', '-f', nargs=1)
parser.add_argument('--justify', '-j')

# Parse the arguments
args = parser.parse_args()
if(not args.feed): args.feed = 3
else: args.feed = int(args.feed[0])

# Setup printer if necessary
if(not args.test):
	printer = adf.Adafruit_Thermal('/dev/serial0', 19200, timeout=5)

# Check font styling
if(not args.test):
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
		if(not args.test): printer.setSize('L')
		line_length = 16
	elif(args.medium):
		if(not args.test): printer.setSize('M')
		line_length = 32
	elif(args.small):
		if(not args.test): printer.setSize('S')
		line_length = 32

# Check justification
if(args.justify and not args.test):
	if(args.justify.lower() == 'l' or args.justify.lower() == 'left'):
		printer.justify('L')
	elif(args.justify.lower() == 'r' or args.justify.lower() == 'right'):
		printer.justify('R')
	elif(args.justify.lower() == 'c' or args.justify.lower() == 'center'):
		printer.justify('C')
	else:
		raise ValueError("Invalid justification option: " + str(args.justify))


''' Iterate through each word and construct a string which will print 
	properly with whole-word text wrapping

	It is better to have the printer print a single string instead of
	having to print multiple strings, so spaces are added to "pad" each
	line to be of the correct length, instead of printing multiple times.
'''
split_text = args.to_print.split(" ") # Split at the spaces
current_length = 0
current_print = ''
for word in split_text:
    if(len(word)+current_length < line_length):
        # If the word fits with room for a space, add both
        current_print += word + " "
        current_length += len(word)+1

    elif(len(word)+current_length == line_length):
        # If only the word fits, add just the word no space after
        current_print += word
        current_length += len(word)        

    else:
        # If the word doesn't fit, we need to add spaces to get to 
        # the next line
        while(current_length != line_length):
            current_print += " "
            current_length += 1

        # Reset current line counter
        current_length = 0

        # Add word which was too long for last line to beginning of this line
        if(len(word) == line_length):
            current_print += word

        elif(len(word)+1 == line_length):
            current_print += word + " "

        elif(len(word)+1 < line_length):
            current_print += word + " "
            current_length += len(word) + 1
        
        elif(len(word) > line_length):
            # Edge case where word is longer than line length
            # Print the word with a hyphen
            # Find the number of lines this word will take
            num_lines = int(math.ceil(len(word)/float(line_length)))
            
            # Iterate for all lines with hyphen
            for i in range(num_lines-1):
                current_print += word[i*(line_length-1):((i+1)*line_length)-1] + '-'
            
            # Add the last line
            word_length = len(word[((num_lines-1)*line_length)-1:])
            if(word_length == line_length):
                current_print += word[((num_lines-1)*line_length)-1:]
                current_length = 0
            elif(word_length+1 == line_length):
                current_print += word[((num_lines-1)*line_length)-1:] + ' '
                current_length = 0
            elif(word_length+1 < line_length):
                current_print += word[((num_lines-1)*line_length)-1:] + ' '
                current_length = word_length+1


# Print the results
# Cut the rows so the text wraps
# None of the text formatting changes width, just text size
if(args.test):
    print("Parsed: " + str(args))
    print("Printing: " + str(current_print))
    print("Feed: " + str(args.feed) + ", type: " + str(type(args.feed)))

if(not args.test):
	printer.println(current_print) # Print text
	printer.feed(args.feed) # Feed required amount
	printer.setDefault() # Return to default settings
