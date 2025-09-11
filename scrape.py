import os
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_subjects(page):
    information=requests.get(page)
    soup=BeautifulSoup(information.content,'html.parser')
    subj_values=[]

    subj=soup.find('select',attrs={'name':'p_subj'})
    if subj:
        for option in subj.find_all('option'): 
            subj_values.append(option['value'])
    return subj_values

def get_terms(page):
    information=requests.get(page)
    soup=BeautifulSoup(information.content,'html.parser')
    term_values=[]
    term=soup.find('select',attrs={'name':'p_term'})
    if term:
        for option in term.find_all('option'):
            term_values.append(option['value'])
    return term_values

def get_data(subj_values,target_term,semester):
    class_dir="class_list"
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)
    filename=os.path.join(class_dir,f"classes_{semester}.pkl")
    if os.path.exists(filename):
        print(f"Loading data from {filename}")
        return load_data(filename,semester)
    else:
        print(f"Fetching data")
        dataframes=[]
        for subj_value in subj_values:
            try:
                response=requests.get(f'https://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term={target_term}&p_subj={subj_value}')
                html=response.text
                datafram=pd.read_html(StringIO(html))
                dataframes.append(datafram[0])
            except:
                pass
        classes=clean_data(dataframes)
        save_data(classes,semester)
        return classes
def clean_data(dataframes):
    if not dataframes:
        print("No data received")
        return pd.DataFrame()
    clean_data=[]
    for df in dataframes:
        df=df.dropna(subset=['Course','Title','Instructor'],how='all')
        keep_columns=['CRN','Course','Days','Date','Time','Location','Type','Title','Instructor']
        if not all(col in df.columns for col in keep_columns):
            print("Skipping dataframe due to missing column")
            continue
        df=df[keep_columns]
        cons_row=[]
        i=0
        while i<len(df):
            current_row=df.iloc[i].copy()
            has_only_instr=(pd.isna(current_row.get('CRN'))and pd.isna(current_row.get('Course'))and pd.isna(current_row.get('Type')) and pd.isna(current_row.get('Title'))and pd.notna(current_row.get('Instructor')))
            if has_only_instr and i>0 and len(cons_row)>0:
                prev_row=cons_row[-1].copy()
                if(pd.notna(current_row['Instructor'])and current_row['Instructor']not in str(prev_row['Instructor'])):
                    prev_row['Instructor']=f"{prev_row['Instructor']},{current_row['Instructor']}"
                    cons_row[-1]=prev_row
                    i+=1
            else:
                cons_row.append(current_row)
                i+=1
        df=pd.DataFrame(cons_row)
        for col in ['CRN','Course','Title']:
            df[col]=df[col].ffill()
        df['CRN']=df['CRN'].fillna('').astype(str)
        df['BaseCourse']=df['Course'].str.split('-').str[0].str.strip()
        clean_data.append(df)
    classes=pd.concat(clean_data,ignore_index=True)
    return classes
def save_data(data,semester):
    class_dir="class_list"
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)
    filename=os.path.join(class_dir,f"classes_{semester}.pkl")
    data.to_pickle(filename)
def load_data(data,semester):
    class_dir="class_list"
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)
    filename=os.path.join(class_dir,f"classes_{semester}.pkl")
    data=pd.read_pickle(filename)
    return data
