from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/searchManga")
def search():
    data = request.json
    text = data['text']
    return "<p>Hello, World!</p>"

@app.post("/downloadImage")
def downloadImage():
    data = request.json
    url = data['url']
    res = requests.get(url, headers={'referer': 'https://chapmanganelo.com/'}, stream=True)
    # if res.status_code == 200:
    #     with open('imagendescargada.jpg', 'wb') as f:
    #         for chunk in res:
    #             f.write(chunk)     
    return res.content

@app.post("/getMangaInfo")
def getMangaInfo():
    return ""