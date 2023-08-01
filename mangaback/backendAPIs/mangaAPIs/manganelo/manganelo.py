import re
import json
import io
import time
import requests

from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

scrapperManganeloAPI = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/si"

@app.route("/")
def info():
    return "<p>Manganelo Scrapper v1</p>"

@app.post("/searchManga")
def searchManga():
    """
    Parameters: manga
    Returns an array[] like:
    [
        {
            "name": ""
            "chapters_url": "",
            "image_url": "",
        }
    ]
    """
    data = request.json
    searchQuery = data['manga']
    searchQuery = re.sub(r'\ ','_',searchQuery) # replace whitespaces with underscores
    searchQuery = searchQuery.lower() # uncapitalize
    body = {"url": "https://m.manganelo.com/search/story/"+searchQuery}
    res = requests.post(scrapperManganeloAPI+"/get-manga-info", json=body)
    res.raise_for_status()
    return json.loads(res.content)

@app.post("/getMangaChapters")
def getMangaChapters():
    """
    Parameters: url
    Returns an array[] like:
    [
        {
            "name": "",
            "url": ""
        }
    ]
    """
    data = request.json
    mangaURL = data['url']
    body = {"url": mangaURL}
    res = requests.post(scrapperManganeloAPI+"/get-manga-chapters", json=body)
    res.raise_for_status()
    results = json.loads(res.content)['search_items']
    results.reverse() # Reverse because site goes lastest-first
    return results

@app.post("/getChapterURLS")
def getChapterURLS():
    """
    Parameters: url
    Returns an array[] like:
    [
        "url": ""
    ]
    """
    data = request.json
    chapterURL = data['url']
    body = {"url": chapterURL}
    res = requests.post(scrapperManganeloAPI+"/get-manga-urls", json=body)
    res.raise_for_status()
    return json.loads(res.content)

@app.post("/getImageBlob")
def getImageBlob():
    """
    Parameters: url
    Returns a single binary image
    """
    data = request.json
    url = data['url']
    res = requests.get(url, headers={'referer': 'https://chapmanganelo.com/'})
    res.raise_for_status()    
    imgBlob = res.content
    buffer = io.BytesIO(imgBlob)
    response = send_file(buffer, mimetype='image/jpeg')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)