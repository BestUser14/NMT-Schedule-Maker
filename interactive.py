from filter import to_minutes
from input import *


def select_schedule(schedules):
    if not schedules:
        print("No schedules to select from")
        return None
    display_schedules(schedules)
    while True:
        try:
            choice=input(f"\nSelect a schedule (1-{len(schedules)}) or 'q' to quit: ")
            if choice.lower()=='q':
                    return None
            choice=int(choice)
            if 1<=choice<=len(schedules):
                    return schedules[choice-1]
            else:
                    print(f"Please enter a number between 1 and {len(schedules)}")
        except ValueError:
            print("Please enter a valid number")

def display_schedule_grid(schedule):
    days=['M','T','W','R','F','S','U']
    time_slots=[f"{h:02d}{m:02d}"for h in range(7,21) for m in [0,30]]
    grid=[[" "*15 for _ in range(len(days))] for _ in range(len(time_slots))]
    for _,class_row in schedule.iterrows():
        class_days=str(class_row['Days']).split()
        start,end=to_minutes(class_row['Time'])
        for day in class_days:
            if day in days:
                day_idx=days.index(day)
                for i,slot_time in enumerate(time_slots):
                    slot_minutes=int(slot_time[:2])*60+int(slot_time[2:])
                    if start<=slot_minutes<end:
                        if len(grid[i][day_idx].strip())==0:
                            grid[i][day_idx]=class_row['Course'][:15].ljust(15)
                        else:
                            grid[i][day_idx]="CONFLICT".ljust(15)
    print(" "*5+" ".join(f"{day:^15}" for day in days))
    for i,row in enumerate(grid):
        time_str=f"{time_slots[i][:2]}:{time_slots[i][2:4]}"
        print(f"{time_str:>4} "+" ".join(row))
