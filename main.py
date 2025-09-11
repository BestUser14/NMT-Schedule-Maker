import copy
import json

from calendars import *
from filter import generate_schedule
from input import *
from interactive import *
from scrape import clean_data, get_data, get_subjects, get_terms, save_data


def main():
    page="https://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
    subj_values=get_subjects(page)
    term_values=get_terms(page)

    semester=get_semester()
    classes=get_data(subj_values,semester,semester)
    professor_pref=get_professor_preference('professor.json')
    blocked_times=get_time_blocks('block_time.json')
    target_classes=get_class_preference('classes.json')
    schedules=generate_schedule(classes,target_classes,professor_pref,blocked_times)
    selection=select_schedule(schedules)
    display_schedule_grid(selection)
    export_to_calendar(selection)
main()
