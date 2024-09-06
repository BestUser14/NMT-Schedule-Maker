import requests
import json


#this file uses 4 spaces instead of tab, no other file uses spaces


subjects = ['ACCT','AE','AFAS','ARTH','ARTS','BIOL','BMST','BIOT','BFIN','CH E', 'CHEM', 'CE', 'COMM', 'CEFA', 'CEPR', 'CONC', 'CSE', 'CYBS', 'ECON', 'EDUC', 'EE', 'EMGT', 'ES', 'ENGL', 'ENTR', 'ENVS', 'EXPL', 'FDMA', 'GNDR', 'GEOB', 'GEOC', 'GEOL', 'GEOP', 'GRMN', 'GEX', 'HIST', 'HUMA', 'HYDR', 'IT', 'MGMT', 'MTLS', 'MATH', 'MENG', 'ME', 'MUSC', 'MUSV', 'OPTC', 'PETR', 'PHIL', 'PHYS', 'POLS', 'PORT', 'PSYC', 'PCOM', 'STCH', 'SOSC', 'SPAN', 'TCOM', 'THEA']
#f = open('text.txt','r')
#text = f.read()

#index = text.find('<th align="left" dp="6"><font color="white">Bookstore Link</font></th>')

#newtext = text[index+82:]

#print(newtext)


def parse(array,index):
    #print(array)
    has_recitation=0
    jerson = {}
    jerson["CRN"] = array[index][4:-5]
    temp_string = array[index+1][4:-5]
    temp_list = temp_string.split(' ') #Chem E is CH E because of course it is
    jerson["subject"]=' '.join(temp_list[:-1])
    jerson["class"]=temp_list[-1]
    jerson["campus"]=array[index+2][19:-5]
    jerson["days"]=array[index+3][19:-5].replace(" ","")
    jerson["date"]=array[index+4][19:-5]
    jerson["time"]=array[index+5][4:-5]
    jerson["location"]=array[index+6][4:-5]
    jerson["hrs"]=array[index+7][19:-5]
    jerson["title"]=array[index+9][4:-5]
    jerson["instructor"]=array[index+10][4:-5]
    jerson["seats"]=array[index+11][18:-5]
    jerson["limit"]=array[index+12][18:-5]
    jerson["enroll"]=array[index+13][18:-5]
    jerson["waitlist"]=array[index+14][18:-5]
    jerson["fee"]=array[index+15][18:-5]
    jerson["link"]=array[index+16][28:-39]
    if(len(array)<=index+22):
        pass
    elif(array[index+22]== '<td align="center"></td>'):
        jerson["ta"]=array[index+29][4:-5]
        has_recitation=-1
    elif(array[index+22][:19] == '<td align="center">'):
        has_recitation=1
        jerson["recitation_days"]=array[index+22][19:-5].replace(" ","")
        jerson["recitation_date"]=array[index+23][19:-5]
        jerson["recitation_time"]=array[index+24][4:-5]
        jerson["recitation_location"]=array[index+25][4:-5]
    return json.dumps(jerson),has_recitation

def super_parse(array):
    index=0
    listy = []
    while(index+18<len(array)):
        temp,recitation=parse(array,index)
        listy.append(json.loads(temp))
        index+=22
        if(recitation==1):
            index+=19
        if(recitation==-1):
            index+=19
    try:
        temp,recitation=parse(array,index) #This is where the sandia off campus class breaks
                                           #If i fixed the sandia class there wouldnt be a try and except here
        listy.append(json.loads(temp))
    except:
        pass
        #print(array[index:])
    
    return(listy)

def parse_subject(subject,semester):
    page = requests.get('https://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff?p_term='+semester+'&p_subj='+subject)
    if page.text.find('<table')==-1:
        return
    index = page.text.find('<th align="left" dp="6"><font color="white">Bookstore Link</font></th>')
    newtext = page.text[index+82:]
    index=newtext.find("</table>")
    newtext = newtext[0:index]
    #f = open(subject+'.txt','w')
    #f.write(newtext)
    array = newtext.splitlines(keepends=False)
    #jerson = {"CRN":"20492","subject":"ENGL","class":"1110-01","campus":"M","days":"MWF","date":"08/14/2023-12/08/2023","time":"1000-1050","location":"SPEARE 117","hrs":"3","title":"Composition I","instructor":"Eric D. Lackey","seats":"0","limit":"20","enroll":"20","waitlist":"0","fee":"$25","link":"link"}
    #jason = json.dumps(jerson)

    return super_parse(array)

def parse_semester(semester):
    print("this will take some time")
    classes = {}
    for i in range(len(subjects)):
        classes[subjects[i]] = parse_subject(subjects[i],semester)
    return classes

def fast_parse(semester):
    try:
        f = open('class_lists/' + semester+'.json','r')
        jerson = json.loads(f.read())
        f.close()
    except:
        jerson = parse_semester(semester)
        f = open('class_lists/' + semester+'.json','w+')
        f.write(json.dumps(jerson))
        f.close()
    return jerson
#jarson = parse_semester("202520")
#f = open("classes.json","w+")
#f.write(json.dumps(jarson))
#f.close()
