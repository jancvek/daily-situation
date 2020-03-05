from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

from urllib.parse import urlparse, parse_qs

from os import curdir, sep
import json

import os

currPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(currPath)
libPath = parentPath+'/jan-lib'

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, libPath)

import jan_sqlite
import daily_situation

PORT = 7777

class Handler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        print(self.path)

        try:  
            # if self.path.endswith('.html'): 
            if self.path.endswith('/'):   
                print("v defaultnem pathu")
                self.path = "index.html"
                print(curdir + sep +self.path)
                f = open(curdir + sep +self.path) #open requested file  
                # print(os.getcwd())
                # f = open("index.html")

                #send code 200 response  
                self.send_response(200)  
        
                #send header first  
                self.send_header('Content-type','text-html')  
                self.end_headers()  
        
                #send file content to client  
                fileData = f.read()
                self.wfile.write(fileData.encode('utf-8'))  
                f.close()  
                return

            elif self.path.find('getData') > -1:
                #send code 200 response  
                self.send_response(200)

                #send header first  
                self.send_header('Content-type', 'application/json')
                self.end_headers()    

                resDate = daily_situation.getDailySituationMailn()

                jsonData = json.dumps(resDate)
                mBin = jsonData.encode('utf-8')

                self.wfile.write(mBin) 

            # elif self.path.endswith('/saveData'):
            elif self.path.find('saveData') > -1:
                print("v saveData pathu")

                print(self.path.find('saveData'))

                print(self.path)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                query_parameters = parse_qs(urlparse(self.path).query)
                
                id = None
                filling = ''
                sex = ''
                a_init = ''
                red_day = ''
                additional = ''

                if 'id' in query_parameters:
                    id = query_parameters["id"][0]
                else:
                    print("parameter id je nujen!")
                    
                    mStr = json.dumps({"error": "NI ID PODATKA"})
                    mBin = mStr.encode('utf-8')
                    self.wfile.write(mBin)  
                    return
                if 'filling' in query_parameters:
                    filling = query_parameters["filling"][0] #return -> ['21'] so ve need to add [0]
                if 'sex' in query_parameters:
                    sex = query_parameters["sex"][0]
                if 'a_init' in query_parameters:
                    a_init = query_parameters["a_init"][0]
                if 'red_day' in query_parameters:
                    red_day = query_parameters["red_day"][0]
                if 'additional' in query_parameters:
                    additional = query_parameters["additional"][0]

                sqlConn = jan_sqlite.create_connection(currPath+"/data.db")

                # values = ('1','MASA',str(cobissMasa.status.name),cobissMasa.minDays,cobissMasa.error)
                values = (int(filling), int(sex), int(a_init), int(red_day), additional)
                res = daily_situation.updateDailySituation(id, values)

                mStr = json.dumps({"status": "OK"})
                mBin = mStr.encode('utf-8')
                self.wfile.write(mBin)  
                return

            elif self.path.endswith(".js"):
                f = open(currPath + sep +self.path, 'rb')
                #send code 200 response  
                self.send_response(200)  

                #send header first  
                self.send_header('Content-type','application/javascript')
                self.end_headers()  

                fileData = f.read()
                self.wfile.write(fileData)  
                f.close()  
                return

        except IOError:  
            self.send_error(404, 'file not found')  

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', PORT), Handler) #uporabi 'localhost' če želiš dovoliti dostop le na host-u
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()