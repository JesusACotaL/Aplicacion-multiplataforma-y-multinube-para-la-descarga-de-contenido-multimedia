from flask import Flask, request, jsonify
import requests

from myanimelistScrapper import scrapManga, searchMangaOnline

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/searchManga")
def searchMangaAnimelist():
    data = request.json
    query = data['manga']
    mangas = searchMangaOnline(query)
    return jsonify(mangas)

@app.post("/getMangaInfo")
def getMangaInfoAnimelist():
    data = request.json
    url = data['url']
    mangaInfo = scrapManga(url)
    return jsonify(mangaInfo)

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