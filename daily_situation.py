import json
import os

currPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(currPath)
libPath = parentPath+'/jan-lib'

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, libPath)

import jan_sqlite


def getDailySituationMailn():

    sqlConn = jan_sqlite.create_connection(currPath+"/data.db")

    with sqlConn:
        # data = jan_sqlite.get_data_all(sqlConn,'data')
        data = jan_sqlite.run_query(sqlConn, "SELECT * FROM data WHERE is_complete = '0'")
        
    dataList = []   
    for a in data:
        d = {"id": a[0], "day": a[1], "is_complete": a[2], "filling": a[3], "sex": a[4], "a_init": a[5], "red_day": a[6], "additional": a[7]}
        dataList.append(d)

    returnObj = {
        "data": dataList
    }

    dJson = json.dumps(returnObj)

    print(dJson)

    return dJson

    # def addDailySituationToday():
        # date format -> 2019-12-30 08:30:40