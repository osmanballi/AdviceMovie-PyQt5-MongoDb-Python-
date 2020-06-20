#for country names
import csv
def countries():
    with open("countries.csv") as f:
        okur = csv.reader(f)
        list=[]
        for satır in okur:
            list.append(satır[0])
    return list
    
def actors():
    with open("actors.csv") as f:
        okur = csv.reader(f)
        list=[]
        for satır in okur:
            list.append(satır[0])
    return list





        