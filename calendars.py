import re
from datetime import datetime, timedelta

import pytz
from icalendar import Calendar, Event


def export_to_calendar(schedule,filename="schedule.ics"):
    cal=Calendar()
    semester_start=None
    semester_end=None

    day_mapping={'M':0,'T':1,'W':2,'R':3,'F':4,'S':5,'U':6}
    for _,class_row in schedule.iterrows():
        date_str=str(class_row.get('Date',''))
        if date_str and 'to' in date_str.lower() or '-' in date_str:
            date_range=re.split(r'[-–—to]+',date_str,flags=re.IGNORECASE)
            if len(date_range)>=2:
                try:
                    for fmt in ['%m/%d/%Y','%Y-%m-%d','%m-%d-%Y']:
                        try:
                            start_cand=datetime.strptime(date_range[0].strip(),fmt).date()
                            end_cand=datetime.strptime(date_range[1].strip(),fmt).date()
                            if semester_start is None or start_cand<semester_start:
                                semester_start=start_cand
                            if semester_end is None or end_cand>semester_end:
                                semester_end=end_cand
                            break
                        except ValueError:
                            continue
                except (ValueError,IndexError):
                    pass
    for _,class_row in schedule.iterrows():
        event=Event()
        event.add('summary',class_row.get('Course'))
        event.add('location',class_row.get('Location','TBD'))
        event.add('description',f"Instructor: {class_row.get('Instructor')}")

        start_str,end_str=class_row['Time'].split('-')
        start_time=datetime.strptime(start_str,'%H%M').time()
        end_time=datetime.strptime(end_str,'%H%M').time()

        days=str(class_row['Days']).split()
        for day in days:
            if day in day_mapping:
                first_day=semester_start+timedelta(days=(day_mapping[day]-semester_start.weekday())%7)
                current_date=first_day
                while current_date<=semester_end:
                    event_start=datetime.combine(current_date,start_time)
                    event_end=datetime.combine(current_date,end_time)
                    event.add('dtstart',event_start)
                    event.add('dtend',event_end)
                    event.add('rrule',{'freq':'weekly','until':semester_end})
                    current_date+=timedelta(weeks=1)
        cal.add_component(event)
    with open(filename,'wb') as f:
        f.write(cal.to_ical())
    print(f"Calendar exported to {filename}")
