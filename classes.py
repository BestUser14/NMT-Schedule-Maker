import scrape
import json
import copy

def get_semester():
	year = input("enter the year of the semester: ")
	date = input("enter the semester (summer, fall, spring): ")
	date_change = {"summer":"10","fall":"20","spring":"30"}

	if date_change[date]!='30':
		year=str(int(year)+1)
	semester = year+date_change[date]

	return semester

def get_class(clas,semester):
	classs = clas.split(' ')
	subject = ' '.join(classs[:-1])
	number = classs[-1]
	class_list = []
	class_list_recitation=[]
	try:
		f = open('class_lists/' + semester+'.json','r')
		jerson = json.loads(f.read())
		f.close()
	except:
		jerson = scrape.parse_semester(semester)
		f = open('class_lists/' + semester+'.json','w+')
		f.write(json.dumps(jerson))
		f.close()
	for i in range(len(jerson[subject])):
		if number == jerson[subject][i]["class"][:-3]:
			#print(jerson[subject][i]["class"])
			class_list.append(jerson[subject][i])
			if("recitation_days" in jerson[subject][i].keys()):
				recitation = copy.deepcopy(jerson[subject][i])
				recitation["days"] = recitation["recitation_days"]
				recitation["date"] = recitation["recitation_date"]
				recitation["time"] = recitation["recitation_time"]
				recitation["location"] = recitation["recitation_location"]
				recitation["class"] = recitation["class"] + "_recitation"
				class_list_recitation.append(recitation)
	return class_list,class_list_recitation
def get_class_list(class_list, semester):
	full_list = []
	for i in class_list:
		list1,list2=get_class(i, semester)
		full_list.append(list1)
		if len(list2)>0:
			full_list.append(list2)
	return full_list

def class_combo(class_list):
	#class list has full information in it for prof white/blacklist
	counter1 = 1
	counter2 = []
	counter3 = []
	output = []
	temp_output=[]
	temp_time = []
	for x in range(len(class_list)):
		counter1 *= len(class_list[x])
		counter2.append(len(class_list[x])-1)
		counter3.append(0)
	for y in range(counter1):
		for i in range(len(counter3)):
			if("recitation" in class_list[i][counter3[i]]["class"]):
				temp_time.append([class_list[i][counter3[i]]["recitation_days"],class_list[i][counter3[i]]["recitation_time"],(class_list[i][counter3[i]]["class" ] + "_recitation")])
			else:
				temp_output.append(class_list[i][counter3[i]]["subject"] + " " + class_list[i][counter3[i]]["class"])
				temp_time.append([class_list[i][counter3[i]]["days"],class_list[i][counter3[i]]["time"],class_list[i][counter3[i]]["class"]])
		if(time_collide(temp_time)==1):
			output.append(temp_output)
		counter3 = count_up(counter2,counter3)
		temp_output=[]
		temp_time=[]
	return output
def count_up(counter2,counter3):
	counter3[-1]+=1
	for x in range(len(counter3)):
		if(counter3[-1*(x+1)]>counter2[-1*(x+1)]):
			counter3[-1*(x+1)]=0
			if(x!=len(counter3)-1):
				counter3[-1*(x+2)]+=1
		else:
			break
	return counter3
def time_collide(times):
	#print(times)
	#the problem is in this function
	#recitation never appears in collision checks even though it is in the time array
	start_end = []
	start_end2 = []
	for day in ["U","M","T","W","R","F","S"]:
		
		for x in range(len(times)):
			for y in range(len(times)):
				if(x==y):
					pass
				elif((not day in times[x][0]) or (not day in times[y][0])):
					pass
				else:
					start_end = times[x][1].split('-')
					start_end2 = times[y][1].split('-')
					start_end[0] = int(start_end[0])
					start_end[1] = int(start_end[1])
					start_end2[0] = int(start_end2[0])
					start_end2[1] = int(start_end2[1])
					if(start_end[1]<=start_end2[0] and start_end[1] <= start_end2[1] and start_end[0]<=start_end2[1] and start_end[0]>=start_end2[0]):
						#collision
						return -1
					if(start_end[0]<=start_end2[0] and start_end[0]<=start_end2[1] and start_end[1]>=start_end2[0] and start_end[1]<=start_end[1]):
						#("collision")
						return -1
		f = open("block_time.json",'r')
		a = f.read()
		f.close()
		block_times = json.loads(a)
		for x in range(len(block_times[day])):
			for y in range(len(times)):
				start_end = times[x][1].split('-')
				start_end2 = block_times[day][x].split('-')
				start_end[0] = int(start_end[0])
				start_end[1] = int(start_end[1])
				start_end2[0] = int(start_end2[0])
				start_end2[1] = int(start_end2[1])
				if(start_end[1]<=start_end2[0] and start_end[1] <= start_end2[1] and start_end[0]<=start_end2[1] and start_end[0]>=start_end2[0]):
					#collision
					return -1
				if(start_end[0]<=start_end2[0] and start_end[0]<=start_end2[1] and start_end[1]>=start_end2[0] and start_end[1]<=start_end[1]):
					return -1
	return 1
def get_all_classes(classes,semester):
	#class_list=get_class_list(['PHYS 1320', 'CSE 221', 'CSE 241', 'CSE 241L', 'MATH 3082', 'MATH 3082L'], "202520")
	class_list=get_class_list(classes,semester)
	return class_combo(class_list)

def get_all_classes_lazy(semester):
	f = open("classes.json",'r')
	a=f.read()
	f.close()
	return get_all_classes(json.loads(a),semester)

if __name__ == "__main__":
	a=get_all_classes_lazy("202520")
	#print(a)
	print(len(a))
