import copy
import json

from filter import generate_schedule
from scrape import clean_data, get_data, get_subjects, get_terms, save_data


def get_semester():
    year=input("Enter the year of the semester you would like to search: ")
    date=input("Enter the semester you would like to search (summer,fall,spring): ")
    date_change={"summer":"10","fall":"20","spring":"30"}
    if date_change[date]!='30':
        year=str(int(year)+1)
    semester=year+date_change[date]
    return semester
def get_time_blocks(filename):
    with open(filename) as f:
        blocked_times=json.load(f)
    return blocked_times
def get_professor_preference(filename):
    with open(filename) as f:
        pref_prof=json.load(f)
    return pref_prof
def get_class_preference(filename):
    with open(filename) as f:
        target_classes=json.load(f)
    return target_classes

def display_schedules(schedules):
    if not schedules:
        print("No valid schedules found")
        return
    print(f"\n Found {len(schedules)} possible schedules: ")
    print("="*80)
    for i,schedule in enumerate(schedules,1):
        print(f"\nSCHEDULE {i}:")
        print("-"*40)
        schedule_display=schedule[['Course','Days','Time','Location','Instructor']].copy()
        print(schedule_display.to_string(index=False))
        print(f"Total courses: {len(schedule)}")
        print("-"*40)

