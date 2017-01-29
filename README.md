# Daily-Briefing
McHacks Project

In order to use this software, you must have an ardunio connected to the computer which is running the included arduino program. The computer can then run the python program to grab data and push it to the printer.  On the arduino the printer should be connected to ground, Rx to pin 6 and Tx to pin 5.  Praw is necessary to run the python file, and can be installed using the pip package manager.

To run the server, configure the app.py file to include a secret key at the top. Running app.py will start the server on port 5000. 
