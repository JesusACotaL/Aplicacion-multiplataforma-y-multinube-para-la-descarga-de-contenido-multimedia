"""
MAIN API ENDPOINT for Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0
pip install -r requirements.txt
pip freeze > requirements.txt
"""
from main import *
import webbrowser
from waitress import serve
import time
import socket
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
port = find_free_port()

print('Serving on 0.0.0.0:'+str(port))
webbrowser.open('http://127.0.0.1:'+str(port),new=0, autoraise=True)
serve(app, host='0.0.0.0', port=port)