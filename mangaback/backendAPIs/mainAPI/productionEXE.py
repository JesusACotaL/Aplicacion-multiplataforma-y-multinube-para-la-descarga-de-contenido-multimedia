"""
MAIN API ENDPOINT for Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0
pip install -r requirements.txt
pip freeze > requirements.txt
"""
from main import app
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

port = 8080 # For whatever reason, we get 404 unless in default port?
print('Serving on 127.0.0.1:'+str(port))
webbrowser.open('http://127.0.0.1:'+str(port),new=0, autoraise=True)
#app.run(host='127.0.0.1', port=port, debug=True)
serve(app, host='127.0.0.1', port=port)