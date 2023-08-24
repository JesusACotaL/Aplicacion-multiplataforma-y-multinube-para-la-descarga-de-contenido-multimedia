'''
pip install -r requirements.txt
pip freeze > requirements.txt
'''
from contextlib import closing
import socket
import os
import json
import subprocess
import time

def find_current_IP():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

mangaAPIs = []
for folder in os.listdir('mangaAPIs'):
    mangaAPIs.append({'name': folder})
mangaInfoAPIs = []
for folder in os.listdir('mangaInfoAPIs'):
    mangaInfoAPIs.append({'name': folder})

def startAPIs():
    global mangaAPIs, mangaInfoAPIs
    for source in mangaAPIs:
        wd = os.getcwd()
        os.chdir(wd+'/mangaAPIs/'+source['name'])
        ip, port = find_current_IP(), find_free_port()
        source['url'] = 'http://'+ip+':'+str(port)
        source['process'] = subprocess.Popen('waitress-serve --listen=*:'+str(port)+'main:app',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        print('Serving '+source['name']+' on '+source['url'])
        os.chdir(wd)
        time.sleep(1)
    for source in mangaInfoAPIs:
        wd = os.getcwd()
        os.chdir(wd+'/mangaInfoAPIs/'+source['name'])
        ip, port = find_current_IP(), find_free_port()
        source['url'] = 'http://'+ip+':'+str(port)
        source['process'] = subprocess.Popen('waitress-serve --listen=*:'+str(port)+'main:app',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        print('Serving '+source['name']+' on '+source['url'])
        os.chdir(wd)
        time.sleep(1)

def stopAPIs():
    global mangaAPIs, mangaInfoAPIs
    for source in mangaAPIs:
        source['process'].terminate()
    for source in mangaInfoAPIs:
        source['process'].terminate()

if __name__ == '__main__':
    startAPIs()
    input('Press ENTER to terminate everything...')
    stopAPIs()