# NMT-Schedule-Maker
This program automatically makes schedules for New Mexico Institute of Mining and Technology classes. These schedules can be organized in a few ways based on how the user wants their schedule to be organized, including evenly spreading out classes or minimzing classes on a certain day, as well as preferred professors for classes.

To use this program install python (and possible pip)

On windows:
	go to python.org and install the newewest verison of python3
	go to the command line and type this command
		py -m pip install pytz, ics, datetime, requests
	then you can run the program by running this in the command line in the program folder
		py main.py
On linux (debian):
	run this
		sudo apt install python3
		sudo apt install pip
		python3 -m pip install pytz, ics, datetime, requests
	to run the program run this
		python3 main.py
none of the above was proofread or tested, if it doesnt work, look at the python error and install whatever library it says is missing

To run the program three json files should have values in them that you want

classes.json
	this file should have the name of your class in it, eg. CSE 101
	there should not be a class version. Good: CSE 101. Bad: CSE 101-01
	the file already has an example class list in it, but here it is again
	["PHYS 1320","MATH 3082","CSE 241","CSE 241L", "CSE 221", "PHYS 1320L"]
	
professor.json
	this file has information on what professor you want for the class
	type the professors name exactly as it appears in banweb
	for example, if you want Steve P. Jobs for physics 2, this would be one of the elements in the json:
		"PHYS 1320":["Steve P. Jobs",1]
	if you want any professor except for Steve P. Jobs for physics 2, this would be one of the elements in the json:
		"PHYS 1320":["Steve P. Jobs",0]
	here is an example json with two professor preferences
		{"CSE 101":["Steve P. Jobs",1],"PHYS 1320":["Steve P. Jobs",0]}
	in this example you want Steve P. Jobs for CSE 101 but you want anyone else for PHYS 1320

block_time.json:
	this json is to block time slots for clubs or work or break times or whatever. If you dont want a class during a time period then put that time in this file.
	use military time, eg. 2pm is 1400.
	time ranges should be written as this: 1200-1300 (12pm to 1pm)
	0 is 12am the day of and 24 is 12am of the next day. 0000-0800 is no class before 8am and 1700-2400 is no class after 5pm
	the json has times for monday through sunday (U). you can put multiple times like this
		['1200-1300','1430-1530']
	here is an example json for the whole week with no classes before 9am and no classes after 3pm on fridays.
		{"M":["0000-0900"],"T":["0000-0900"],"W":["0000-0900"],"R":["0000-0900"],"F":["0000-0900","1500-2400"],"S":["0000-0900"],"U":["0000-0900"]}


Calendar
	This program export the schedule into an ics file which can be read by basically any calendar app.
	when you import the calendar, it is probably a good idea to make a new calendar in the calendar, which can be done in at least: apple calendar, google calendar, ubuntu calendar.
	you can use this new calendar to see the schedule, and if you dont like it you can just delete that calendar instead of manually deleting hundreds of classes from your personal events.
	to use the calendar you can open the ics file in your calendar app and save it to your temporary calendar.
