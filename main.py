import calendars
import classes
import optimise
import scrape

semester = classes.get_semester()

optimizer = int(input("enter 1 to optimize for least classes on a day, 2 to spread classes out evenly, and 3 to avoid TR classes: "))
do_prof_optimize = int(input("enter 1 to select professors according to professor.json: "))
clases = []
if optimizer == 1:
	day = int(input("enter the number for what day you want to have the least classes (1 is monday, 5 is friday, 0 is any class: "))
	clases = optimise.min_class_day(semester,day)
elif optimizer == 2:
	clases = optimise.even_split(semester)
elif optimizer ==3:
	clases = optimise.no_tuesday(semester)
else:
	clases = classes.get_all_classes_lazy(semester)
if do_prof_optimize == 1:
	clases = optimise.optimize_prof(clases,semester)
old_view=-100
while((view := int(input("what schedule number would you like to see. There are " + str(len(clases)) + " classes: "))-1)!=old_view):
	old_view=view
	optimise.show_cal(clases[view],semester)
	print("enter the same schedule to select it")

print(clases[view])
if len(clases) == 0:
	print("there are no schedules with these optimizations")
else:
	calendars.make_calendar(clases[view],semester)
	
	print('\n')
	for i in range(len(clases[view])):
		optimise.print_class_information(clases[view][i], semester)
	print("\ncheck the schedule in the schedules folder. delete the jsons in class_lists and check the classes again before the semester starts in case the location for the class changes.")