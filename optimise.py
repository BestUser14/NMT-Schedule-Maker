import json
import statistics
import classes
import calendars
days = ['N','M','T','W','R','F'] #N should never appear
day_to_number = {"M":0,"T":1,"W":2,"R":3,"F":4}
def min_class_day(semester,min_day):
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
	return sorted(classes.get_all_classes_lazy(semester),key=fancy_stddev) #[:number_to_view-1]
def fancy_stddev(clas):
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
	print(str(classs["subject"]) + " " + str(classs["class"]))
	print("CRN " + str(classs["CRN"]))
	print("seats, limit, enroll:   " + str(classs["seats"]) + ", " + str(classs["limit"]) + ", " + str(classs["enroll"]) + "    waitlist " + str(classs["waitlist"]))
	print('')
	
if __name__ == "__main__":
	#semester = classes.get_semester()
	semester = '202520'
	#lis = min_class_day(semester,0)
	#real_class = lis[0]
	#calendars.make_calendar(real_class,semester)
	#calendars.make_calendar(even_split(semester)[0],semester)
	calendars.make_calendar(optimize_prof(semester)[0],semester)
