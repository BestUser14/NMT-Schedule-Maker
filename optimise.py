import json
import statistics
import classes
import calendars
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
days = ['N','M','T','W','R','F'] #N should never appear
day_to_number = {"M":0,"T":1,"W":2,"R":3,"F":4}
def min_class_day(semester,min_day):
	#can be condensed like in no_tuesday
	class_list = classes.get_all_classes_lazy(semester)
	results = []
	small_amount = 100
	temp_amount = 0
	if min_day == 0:
		for day in days[1:]:
			for x in range(len(class_list)):
				for y in range(len(class_list[x])):
					if day in calendars.find_class(class_list[x][y],semester)["days"]:
						temp_amount+=1
				if temp_amount<small_amount:
					small_amount = temp_amount
				temp_amount = 0
		for day in days[1:]:
			for x in range(len(class_list)):
				for y in range(len(class_list[x])):
					if day in calendars.find_class(class_list[x][y],semester)["days"]:
						temp_amount+=1
				if temp_amount == small_amount:
					results.append(class_list[x])
				temp_amount = 0
					
	else:
		day = days[min_day]
		for i in range(len(class_list)):
			for x in range(len(class_list[i])):
				if day in calendars.find_class(class_list[i][x],semester)["days"]:
					temp_amount+=1
			if temp_amount<small_amount:
				small_amount = temp_amount
			temp_amount=0
		for i in range(len(class_list)):
			for x in range(len(class_list[i])):
				if day in calendars.find_class(class_list[i][x],semester)["days"]:
					temp_amount+=1
			if temp_amount == small_amount:
				results.append(class_list[i])
			temp_amount=0
	print("found " + str(len(results)) + " results with " + str(small_amount) + " classes on a certain day")
	return results
def even_split(semester):
	return sorted(classes.get_all_classes_lazy(semester),key=lambda cl: fancy_stddev(cl,semester)) #[:number_to_view-1]

def no_tuesday(semester):
	class_list = classes.get_all_classes_lazy(semester)
	results = []
	small_amount = 100
	temp_amount=0
	for x in range(len(class_list)):
		for y in range(len(class_list[x])):
			if ('T' in calendars.find_class(class_list[x][y],semester)["days"]) and ('R' in calendars.find_class(class_list[x][y],semester)["days"]):
				temp_amount+=1
		if temp_amount<small_amount:
			results = []
			small_amount = temp_amount
			results.append(class_list[x])
		if temp_amount==small_amount:
			results.append(class_list[x])
		temp_amount=0
	print("found " + str(len(results)) + " results with " + str(small_amount) + " TH classes")
	return results

def fancy_stddev(clas,semester):
	temp = [0,0,0,0,0]
	for i in range(len(clas)):
		for day in calendars.find_class(clas[i],semester)["days"]:
			temp[day_to_number[day]]+=1
	return statistics.stdev(temp)
def optimize_prof(class_list,semester):
	f = open('professor.json','r')
	profs = json.loads(f.read())
	f.close()
	classy = []
	for y in range(len(class_list)):
		for i in range(len(class_list[y])):
			for x in list(profs.keys()):
				if x == class_list[y][i][:-3]:
					if bool(profs[x][0] == calendars.find_class(class_list[y][i],semester)["instructor"]) == bool(profs[x][1]):
						classy.append(class_list[y])
	print("found " + str(len(classy)) + " schedules with the selected professors")
	return classy
def print_class_information(clas,semester):
	classs = calendars.find_class(clas,semester)
	print("Title: " + str(classs["title"]))
	print(str(classs["subject"]) + " " + str(classs["class"]))
	print("CRN " + str(classs["CRN"]))
	print("Days " + str(classs["days"]))
	print("Time " + str(classs["time"]))
	print("Location " + str(classs["location"]))
	print("seats, limit, enroll:   " + str(classs["seats"]) + ", " + str(classs["limit"]) + ", " + str(classs["enroll"]) + "    waitlist " + str(classs["waitlist"]))
	print("hours " + str(classs["hrs"]))
	print('')

def show_cal(class_list,semester):
	classes=[]
	height=8
	width=10
	plt.figure(figsize=(width,height))
	plt.xlim(1,8)
	plt.ylim(800,2200)
	plt.yticks([800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200])
	plt.gca().invert_yaxis()
	plt.grid()
	plt.xlabel("Day of week")
	plt.ylabel("Time")
	plt.title("Schedule")
	ax=plt.gca().axes
	for i in class_list:
		classs = calendars.find_class(i,semester)
		for day in classs["days"]:
			time=classs["time"]
			start=(time.split('-')[0])
			end=(time.split('-')[1])
			new_start=(int(start[0:2])*100)+(int(start[2:4])*1.6666666666)
			new_end=(int(end[0:2])*100)+(int(end[2:4])*1.6666666666)
			ax.add_patch(Rectangle((day_to_number[day]+2,new_start),1,new_end-new_start))
	plt.show()
	plt.savefig("schedules/calendar.png")
	
if __name__ == "__main__":
	#semester = classes.get_semester()
	semester = '202520'
	#lis = min_class_day(semester,0)
	#real_class = lis[0]
	#calendars.make_calendar(real_class,semester)
	#calendars.make_calendar(even_split(semester)[0],semester)
	calendars.make_calendar(optimize_prof(semester)[0],semester)
