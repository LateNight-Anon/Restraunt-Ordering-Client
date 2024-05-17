# Important information
This project is almost complete (the setup.py and waiter.py programs just need to be finished) as part of a school project for year 10 IT, because of this despite the 'alpha build' like nature of it I most likely won't be adding functionality for cross device connections (i.e servers), improve the UI past what basic Tkinter allows, use proper images in the bathroom section of core.py or add any new functionality once the program is finished.

# Restraunt Ordering Client
This repository contains the source code for 3 pieces of software desiged to work together in a restraunt environment.
Core.py is the main piece, meant to fill a similar place to the ordering terminals in McDonalds; it takes its basic functionality and combines it with the ability to call a waiter to your table, open a map to the bathroom and pay with split billing.
Waiter.py is designed to be used by staff, it shows a live feed of what tables need assistance.
Setup.py is a CLI app designed for admins, it allows the user to config files i.e the menu and table number through a CLI process (this portion of codebase was a last minute conclusion thus the codebase is 'spaghetti' at best)

# Example Files and Definitions of Data
The files in the example files folder contains a copy of all the non-code files in the form I was using to test to the software along with a text file showing where the files should be placed for all pieces of software to work

- bathroom.png: the image used in the 'Bathroom' section of the software
- bleep.mp3: default error noise
- tables.json: contains the data for all tables (is they need assistance and too what severity)
- foodItems.json: contains the definitions for each item in the menu
- closeMessage.txt: contains the message shown on the popup question when closing the app
- tableNumber.csv: contains the table number of whatever table this is installed in
- minAndMaxSev.csv: contains the minimum and maximum severity rating a user can input when asking for assistance

# REQUIRMENTS
- A standard installation of python 3.12
- threading, multiprocessing, typing, csv, json, time, tkinter, PIL and os libraries (part of the standard library)
- The pygame library (installed with 'pip install pygame' or 'python -m pip install pygame --user')
- windows 10, windows 11 or Linux with a Desktop environment
