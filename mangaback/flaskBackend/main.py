from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

from myanimelistScrapper import scrapManga, searchMangaOnline
import re

app = Flask(__name__)
CORS(app)

scrapperManganeloAPI = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/si"

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

@app.post("/findMangaSource")
def findMangaSource():
    data = request.json
    manga = data['manga']
    # Manganelo source
    manga = re.sub(r'\ ','_',manga) # replace whitespaces with underscores
    body = {"url": "https://m.manganelo.com/search/story/"+manga}
    res = requests.post(scrapperManganeloAPI+"/get-manga-info", json=body)
    res.raise_for_status()
    return res.content

@app.post("/getMangaChapters")
def getMangaChapters():
    data = request.json
    url = data['url']
    # Manganelo source
    body = {"url": url}
    res = requests.post(scrapperManganeloAPI+"/get-manga-chapters", json=body)
    res.raise_for_status()
    return res.content

@app.post("/getChapterLinks")
def getChapterLinks():
    data = request.json
    url = data['url']
    # Manganelo source
    body = {"url": url}
    res = requests.post(scrapperManganeloAPI+"/get-manga-urls", json=body)
    res.raise_for_status()
    return res.content

@app.post("/downloadChapterImage")
def downloadChapterImage():
    data = request.json
    url = data['url']
    res = requests.get(url, headers={'referer': 'https://chapmanganelo.com/'}, stream=True)
    # if res.status_code == 200:
    #     with open('imagendescargada.jpg', 'wb') as f:
    #         for chunk in res:
    #             f.write(chunk)     
    return res.content