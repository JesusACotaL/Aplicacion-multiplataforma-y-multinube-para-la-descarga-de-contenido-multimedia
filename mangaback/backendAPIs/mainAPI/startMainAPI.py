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
def startMainApi():
    global mainAPI
    port = find_free_port()
    ip, port = find_current_IP(), find_free_port()
    mainAPI = subprocess.Popen('waitress-serve --listen=*:'+str(port)+' '+'main:app',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    url = 'http://'+ip+':'+str(port)
    print('Serving on '+url)
    return url

def stopMainApi():
    global mainAPI
    mainAPI.terminate()

if __name__ == '__main__':
    startMainApi()
    input('Press ENTER to terminate app...')
    stopMainApi()