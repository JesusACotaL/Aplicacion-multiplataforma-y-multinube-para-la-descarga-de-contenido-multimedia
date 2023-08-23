"""
MAIN API ENDPOINT for Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0
pip install -r requirements.txt
pip freeze > requirements.txt
"""
from contextlib import closing
import socket
import os
import json
import webbrowser
import subprocess

def find_current_IP():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

mainAPI=None
def startMainApi(apis=None) -> str:
    global mainAPI
    port = find_free_port()
    wd = os.getcwd()
    os.chdir(wd+'/mainAPI/executable')
    if(apis):
        data = json.dumps(apis)
        with open('endpoints.json','w') as f:
            f.write(data)
    ip, port = find_current_IP(), find_free_port()
    port = 5050 # Always same port
    mainAPI = subprocess.Popen(['executable.exe','-ip',ip,'-p',str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT) #
    url = 'http://'+ip+':'+str(port)
    print('Serving on '+url)
    os.chdir(wd)
    return url

def stopMainApi():
    global mainAPI
    mainAPI.terminate()

if __name__ == '__main__':
    startMainApi()
    input('Press ENTER to terminate app...')
    stopMainApi()