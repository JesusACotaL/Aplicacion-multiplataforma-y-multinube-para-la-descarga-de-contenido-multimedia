"""
This file allows you to create a binary file of this flask aplication, using waitress as the WSGI and pyinstaller.
You need to pass two arguments for the server to start:
- IP (server to run in)
- PORT (listening port on server)
"""
from main import *
from contextlib import closing
import socket
import waitress
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip", type=str)
parser.add_argument("-p", "--port", type=int)
args = parser.parse_args()
ip = args.ip
port = args.port
if(ip and port):
    url = 'http://'+ip+':'+str(port)
    print('Serving on '+url)
    waitress.serve(app, host='0.0.0.0', port=port)