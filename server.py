import cherrypy
import json,requests
from StringIO import StringIO
import time
from ftplib import FTP
import datetime

def open_server():
    ftp = FTP("nrt3.modaps.eosdis.nasa.gov")
    ftp.login("Abd0_salama","Ichbinabdou1")
    y = str(datetime.datetime.now().timetuple().tm_year)+str(datetime.datetime.now().timetuple().tm_yday)
    file_data = read_file(ftp,y)
    open("Nasa file.txt","w").write(file_data)
    lines = file_data.splitlines()[1:]
    arr = []
    for line in lines:

      fields = map(lambda s: s.strip(), line.split(','))
      arr.append({
          "lat": fields[0],
          "lon": fields[1],
      })
    
    json_data = json.dumps(arr, indent=2)
    print json.dumps(arr, indent=2)
    
    return json_data

def read_file(ftp,f):

    r = StringIO()
    while 1:
        try:
            ftp.retrbinary("RETR FIRMS/c6/Global/MODIS_C6_Global_MCD14DL_NRT_"+f+".txt",r.write)
            break
        except:
            print "File is not created yet"
            time.sleep(5)
            continue
    return r.getvalue()

class helloworld(object):
    @cherrypy.expose
    def index(self):
        x = open_server()
        return x

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 8080
cherrypy.quickstart(helloworld())
