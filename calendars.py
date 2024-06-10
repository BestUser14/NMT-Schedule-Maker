import classes
import scrape
import json
import pytz
import copy
from ics import Calendar,Event
from datetime import datetime, timedelta, timezone
daytoclass = ['M','T','W','R','F','S','U']



def make_calendar(class_list,semester):
	cal = Calendar()
	cal.prodid = 'idk what this is'
	cal.version = '0.0.0.0.0.1'
	for i in range(len(class_list)):
		temp = find_class(class_list[i],semester)
		temp_date = temp["date"].split('-')
		start_date = temp_date[0].split('/')
		start = datetime(int(start_date[2]),int(start_date[0]),int(start_date[1]))
		end_date = temp_date[1].split('/')
		end = datetime(int(end_date[2]),int(end_date[0]),int(end_date[1]))
		while(start.date()<end.date()):
			temp_day = daytoclass[start.weekday()]
			if temp_day in temp["days"]:
				ist = pytz.timezone('US/Mountain')
				event = Event()
				event.name = temp["subject"] + ' ' + temp["class"]
				event.begin = ist.localize(start.replace(hour = int(temp["time"][:2]), minute = int(temp["time"][2:4])))
				event.end = ist.localize(start.replace(hour = int(temp["time"][5:7]), minute = int(temp["time"][7:])))
				event.location = temp["location"]
				cal.events.add(event)
			
			start += timedelta(days=1)
		f = open('schedules/' + semester + '.ics','w+')
		f.write(cal.serialize())
		f.close()
def find_class(class_name,semester):
	temp = class_name.split(' ')
	subject = temp[0]
	classs = temp[1]
	is_recitation = 0
	if("recitation" in classs):
		is_recitation=1
		classs = classs[:-11]
		
	class_list = scrape.fast_parse(semester)
	for i in range(len(class_list[subject])):
		if(class_list[subject][i]["class"] == classs):
			if(is_recitation==1):
				recitation = copy.deepcopy(class_list[subject][i])
				recitation["days"] = recitation["recitation_days"]
				recitation["date"] = recitation["recitation_date"]
				recitation["time"] = recitation["recitation_time"]
				recitation["location"] = recitation["recitation_location"]
				recitation["class"] = recitation["class"] + "_recitation"
				return recitation
			return class_list[subject][i]
	return -1

if __name__ == "__main__":
	#semester = classes.get_semester()
	semester = '202520'
	classes = classes.get_all_classes_lazy(semester)
	real_class = classes[0]
	make_calendar(real_class,semester) #main function for this program
