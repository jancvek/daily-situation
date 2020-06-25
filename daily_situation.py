import json
import os
from datetime import date

currPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(currPath)
libPath = parentPath+'/jan-lib'

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, libPath)

import jan_sqlite
import jan_email


def getDailySituationMailn():

    sqlConn = jan_sqlite.create_connection(currPath+"/data.db")

    with sqlConn:
        # data = jan_sqlite.get_data_all(sqlConn,'data')
        data = jan_sqlite.run_query(sqlConn, "SELECT * FROM data WHERE is_complete = '0'")
        
    dataList = []   
    for a in data:
        d = {"id": a[0], "day": a[1], "is_complete": a[2], "filling": a[3], "sex": a[4], "a_init": a[5], "red_day": a[6], "bs": a[7] "additional": a[8]}
        dataList.append(d)

    returnObj = {
        "data": dataList
    }

    return returnObj

# values = ('1','MASA',str(cobissMasa.status.name),cobissMasa.minDays,cobissMasa.error)
def updateDailySituation(id, values):
    # date format -> 2019-12-30 08:30:40

    sqlConn = jan_sqlite.create_connection(currPath+"/data.db")
    
    with sqlConn:
        res = jan_sqlite.update_data_daily_situation(sqlConn, 'data', id, values)

    return res

def addNewDailySituationToday():

    today = date.today()
    dt_string = today.strftime("%Y-%m-%d")

    sqlConn = jan_sqlite.create_connection(currPath+"/data.db")

    # preveri ali za ta dan že obstaja zapis '2020-03-05'
    with sqlConn:
        data = jan_sqlite.run_query(sqlConn, "SELECT * FROM data WHERE data.day = '"+dt_string+"'")

        if len(data) > 0:
            print("zapis za ta dan že obstaja. Zapis ni bil dodan")    
            return    
        
        params = "day,is_complete,filling,sex,a_init,red_day,bs,additional"
        values = (dt_string,'0','0','0','0','0','0','')
        res = jan_sqlite.insert_data(sqlConn,'data',params,values)

def checkForNotify():

    sqlConn = jan_sqlite.create_connection(currPath+"/data.db")

    with sqlConn:
        data = jan_sqlite.run_query(sqlConn, "SELECT * FROM data WHERE is_complete = '0'")

    if len(data) > 3:
        # send email
        email = jan_email.Email()
        email.sentEmail("jan.cvek@gmail.com","Daily Situation API","Vnesi podatke za zadnje dni! www.cvek.eu:7777")