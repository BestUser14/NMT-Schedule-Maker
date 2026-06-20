from itertools import filterfalse, product

import pandas as pd


def to_minutes(t):
    if pd.isna(t):
        return None
    t=t.strip()
    try:
        start_str,end_str=t.split('-')
        start_h,start_m=int(start_str[:2]),int(start_str[2:])
        end_h,end_m=int(end_str[:2]),int(end_str[2:])
        start_min=start_h*60+start_m
        end_min=end_h*60+end_m
        return start_min,end_min
    except (ValueError,IndexError):
        return None

def is_time_conflict(time1,time2):
    if time1 is None or time2 is None:
        return False
    start1,end1=time1
    start2,end2=time2
    return max(start1,start2)<min(end1,end2)

def has_conflict(schedule):
    schedule=schedule.copy()
    schedule['TimeRange']=schedule['Time'].apply(to_minutes)
    for i in range(len(schedule)):
        for j in range(i+1,len(schedule)):
            row1=schedule.iloc[i]
            row2=schedule.iloc[j]
            days1_str=str(row1.get('Days',''))if not pd.isna(row1.get('Days')) else ''
            days2_str=str(row2.get('Days','')) if not pd.isna(row2.get('Days')) else ''
            days1=set(days1_str.split())
            days2=set(days2_str.split())
            if not days1.intersection(days2):
                continue
            time_range_1=row1['TimeRange']
            time_range_2=row2['TimeRange']
            if is_time_conflict(time_range_1,time_range_2):
                return True
    return False
def generate_schedule(classes,target_classes,professor_prefs=None,blocked_times=None):
    target_set=set(target_classes)
    filtered=classes[classes['BaseCourse'].isin(target_set)].copy() 
    if professor_prefs:
        filtered=filter_by_professor(filtered,professor_prefs)
    if blocked_times:
        filtered=filter_by_blocked_times(filtered,blocked_times)
    #print(f"Target Classes: {target_classes}")
    #print(f"Matching rows after filter: {len(filtered)}")
    print(filtered[['Course','BaseCourse','Days','Time']].to_string(index=False))
    if filtered.empty:
        print("No matching classes found")
        return []
    try:
        crn_groups=[]
        for crn,group in filtered.groupby('CRN'):
            crn_groups.append(group)
        basecourse_groups={}
        for crn_group in crn_groups:
            base_course = crn_group.iloc[0]['BaseCourse']
            if base_course not in basecourse_groups:
                basecourse_groups[base_course]=[]
            basecourse_groups[base_course].append(crn_group) 
        all_combinations=product(*basecourse_groups.values())
        valid=[]
        for combo in all_combinations:
            schedule_rows=pd.concat(combo,ignore_index=True)
            if not has_conflict(schedule_rows):
                valid.append(schedule_rows)
        return valid
    except KeyError as e:
        print(f"Error grouping by 'BaseCourse': {e}")
        return []
def filter_by_professor(classes,professors):
    filtered_classes=classes.copy()
    for base,(professor_name,preference_type) in professors.items():
        if preference_type==1:
            desired=filtered_classes[(filtered_classes['BaseCourse']==base)&(filtered_classes['Instructor'].str.contains(professor_name,na=False))]['CRN'].unique()
            filtered_classes=filtered_classes[~((filtered_classes['BaseCourse']==base)&~filtered_classes['CRN'].isin(desired))]
        else:
            unwanted=filtered_classes[(filtered_classes['BaseCourse']==base)&(filtered_classes['Instructor'].str.contains(professor_name,na=False))]['CRN'].unique()
            filtered_classes=filtered_classes[~((filtered_classes['BaseCourse']==base)&filtered_classes['CRN'].isin(unwanted))]
    return filtered_classes
def is_time_blocked(time_str,day_str,blocked_times):
    if not time_str or pd.isna(time_str) or day_str not in blocked_times:
        return False
    time_range=to_minutes(time_str)
    if not time_range:
        return False
    start,end=time_range
    for blocked in blocked_times[day_str]:
        blocked_range=to_minutes(blocked)
        if blocked_range:
            blocked_start,blocked_end=blocked_range
            conflict=is_time_conflict((start,end),blocked_range)
            #print(f"Debug: {blocked} ({blocked_start}-{blocked_end})->conflict: {conflict}")
            if conflict:
                return True
    return False
def filter_by_blocked_times(classes,blocked_times):
    #print(f"Debug: {blocked_times}")
    crn_groups=[]
    for crn,group in classes.groupby('CRN'):
        crn_groups.append(group)
    valid_group=[]
    for group in crn_groups:
        group_blocked=False
        for _,row in group.iterrows():
            days_str=str(row.get('Days',''))
            days=days_str.split()
            time_str=row['Time']
    
            for day in days:
                if is_time_blocked(time_str,day,blocked_times):
                    group_blocked=True
                    break
            if group_blocked:
                break
        if not group_blocked:
            valid_group.append(group)
    if valid_group:
        result=pd.concat(valid_group,ignore_index=True)
    else:
        result=pd.DataFrame()
    return result
