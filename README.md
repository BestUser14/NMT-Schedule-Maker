
# NMT-Schedule-Maker
This program automatically makes schedules for New Mexico Institute of Mining and Technology classes. These schedules can be organized in a few ways based on how the user wants their schedule to be organized, including evenly spreading out classes or minimizing classes on a certain day, as well as preferred professors for classes.

```console
    pip install -r requirements.txt
    py main.py
```

To run the program three json files should have values in them that you want

classes.json:
- This file should have the name of your class in it, eg. `CSE 101`
- There should not be a class version. `Good: CSE 101. Bad: CSE 101-01`
- See existing file for example

	
professor.json:
- This file has information on what professor you want for the class
- Type the professors name exactly as it appears in banweb
- For example, if you want Steve P. Jobs for physics 2, this would be one of the elements in the json:
		`"PHYS 1320":["Steve P. Jobs",1]`
	if you want any professor except for Steve P. Jobs for physics 2, this would be one of the elements in the json:
		`"PHYS 1320":["Steve P. Jobs",0]`

block_time.json:
- This json is to block time slots for clubs or work or break times or whatever. If you dont want a class during a time period then put that time in this file.
- Use military time, eg. 2pm is 1400.
	time ranges should be written as this: 1200-1300 (12pm to 1pm)

Calendar:
This program export the schedule into an ics file which can be read by basically any calendar app.
	when you import the calendar, it is probably a good idea to make a new calendar in the calendar, which can be done in at least: apple calendar, google calendar, ubuntu calendar.
	you can use this new calendar to see the schedule, and if you dont like it you can just delete that calendar instead of manually deleting hundreds of classes from your personal events.
	to use the calendar you can open the ics file in your calendar app and save it to your temporary calendar.

Class_lists:
- This program saves scraped classes under the `class_list` folder
- To refresh the data simply remove the corresponding file
