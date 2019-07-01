'''
Python3 library for the Adafruit Thermal Receipt Printer
Requires the printer_wrapper python2 file
'''

import subprocess

def print_text(text, size='medium', bold=False, inverse=False, tall=False, underline=False, feed=3, justify='left'):
    # Generate the base call
    call = 'python2 printer_wrapper.py "' + text + '"'

    # Check for size change
    if(size not in ['large', 'medium', 'small']):
        raise ValueError("Invalid size option: " + str(size))
    call += ' --' + size

    # Check for formatting
    if(bold): call += ' -b'
    if(inverse): call += ' -i'
    if(tall): call += ' -t'
    if(underline): call += ' -u'

    # Check for feed
    if(type(feed) != int):
        raise TypeError("Feed value must be int, found " + str(type(feed)))
    call += ' -f ' + str(feed)

    # Check for justify
    if(justfy not in ['left', 'right', 'center', 'l', 'r', 'c']):
        raise ValueError("Invalid justification option: " + str(justify))
    call += ' -j ' + justify

    # Send call
    subprocess.Popen(call.split())