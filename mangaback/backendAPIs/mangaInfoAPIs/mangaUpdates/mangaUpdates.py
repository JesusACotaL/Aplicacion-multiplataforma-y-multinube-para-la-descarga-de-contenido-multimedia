import re
import json
import io
import time
import urllib
import requests
from bs4 import BeautifulSoup

from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def info():
    return "<p>mangaupdates Scrapper v1</p>"

@app.post("/searchManga")
def searchManga():
    """
    Parameters: manga
    Returns an array[] like:
    [
        {
            "name": ""
            "img": "",
            "short_desc": "",
            "url": "",
            "score": "",
        }
    ]
    """
    data = request.json
    searchQuery = data['manga']

    # Get HTML
    siteUrl = "https://www.mangaupdates.com/series.html"
    parameters = {
        'search': searchQuery
    }
    encodedParams = urllib.parse.urlencode(parameters, doseq=True)
    search_url = siteUrl + '?%s' % encodedParams
    print(search_url)
    res = requests.get(search_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'html.parser')
    html = soup.select('#main_content > div:nth-child(2) > div:nth-child(2) > div.col-12.col-lg-6.p-3.text')

    # Extract data from each one
    mangasFound = []
    for mangaDiv in html:
        manga = {}

        manga['img'] = ''
        selector = mangaDiv.find('img',attrs={'src':True})
        if(selector):
            selector = re.sub(r'/thumb', '', selector['src']) # Instead of that tiny thumbnail, we must remove any resolution parameters
            manga['img'] = selector
        
        name = mangaDiv.select('div:nth-child(2) > div > div:nth-child(1)')[1].find('a',attrs={'alt':'Series Info'}).string
        manga['name'] = name
        
        manga['short_desc'] = ''
        selector = mangaDiv.select('div:nth-child(2) > div > div:nth-child(3)')
        if(len(selector) > 0):
            manga['short_desc'] = selector[0].string

        url = mangaDiv.select('div:nth-child(2) > div > div:nth-child(1)')[0].find('a',attrs={'alt':'Series Info'})['href']
        manga['url'] = url
        
        manga['score'] = ''
        selector = mangaDiv.select('div:nth-child(2) > div > div:nth-child(4) > b')
        if(len(selector) > 0):
            manga['score'] = selector[0].string

        mangasFound.append(manga)
    return mangasFound

@app.post("/getMangaInfo")
def getMangaInfo():
    """
    Parameters: url
    Returns an object like:
    {
        "name": ""
        "originURL": "",
        "date": "",
        "status": "",
        "score": "",
        "popularity_rank": "",
        "site": "",
        "background": "",
        "img": "",
        "genres": [],
        "authors": [],
        "characters": [
            {
                "name": "",
                "role": "",
                "image": "",
                "url": "",
            }
        ]
    }
    """
    data = request.json
    manga_url = data['url']

    # Get HTML
    res = requests.get(manga_url)
    res.raise_for_status()
    html = BeautifulSoup(res.content, 'html.parser')

    manga = {}

    # Original name
    name = html.select('#main_content > div:nth-child(2) > div > div > span.releasestitle.tabletitle')[0].string
    manga['name'] = name

    # Source url
    manga['originURL'] = manga_url

    # Authors
    authors = html.find('b', string='Author(s)').parent.find_next_sibling().find_all('a')
    authors = [element.string for element in authors]
    manga['authors'] = authors

    # Date
    date = html.find('b', string='Year').parent.find_next_sibling().string.strip('\r\n')
    manga['date'] = date

    # Status
    manga['status'] = 'N/A'
    selector = html.find('div', string=' in Country of Origin')
    if(selector):
        selector = selector.parent.parent.next_sibling.next_sibling.string
        if(selector):
            status = re.findall('\((.*?)\)',selector.strip('\r\n'))
            if(len(status) > 0):
                manga['status'] = status[0]

    # Genres
    genresDiv = html.find('b', string='Genre').parent.find_next_sibling().find_all('a')
    genresDiv = genresDiv[:-1] # Remove last element, it is not a genre
    genres = ', '.join([g.string for g in genresDiv])
    genres = (genres + "").split(', ')
    manga['genres'] = genres

    # Characters
    manga['characters'] = []
    
    # Score
    manga['score'] = 'N/A'
    selector = html.find('b', string='User Rating').parent.find_next_sibling().contents[0]
    if(selector.text.strip('\r\n') != 'N/A'):
        manga['score'] = re.findall('[0-9]*[.]?[0-9]',selector.string.strip('\r\n'))[0]
    
    # Popularity rank
    manga['popularity_rank'] = 'N/A'
    selector = html.find('u', string='Monthly')
    if(selector):
        manga['popularity_rank'] = selector.parent.next_sibling.next_sibling.string

    # Oficial site (if exists)
    manga['site'] = ''
    selector = html.find('b', string='Original Publisher').parent.next_sibling.next_sibling.find('a')
    if(selector):
       manga['site'] = selector['href']

    # Background
    manga['background'] = 'N/A'
    selector = html.find('b', string='Description').parent.next_sibling.next_sibling
    if(selector.text.strip('\r\n') != 'N/A'):
        manga['background'] = selector.text.strip('\r\n')

    # Image
    manga['img'] = ''
    img = html.find('b', string='Image').parent.next_sibling.next_sibling.find('img',attrs={'src':True})
    if(img):
        manga['img'] = img['src']

    return manga

@app.post("/getTopMangas")
def getTopMangas():
    """ 
    Returns a url list of top site mangas
    []
    """
    data = request.json
    limit = int(data['limit'])
    currentPage = 1
    pageAmount = limit / 50
    urls = []
    while(currentPage <= pageAmount):
        # Request search
        url = 'https://www.mangaupdates.com/series.html?orderby=rating&perpage=50'
        res = requests.get(url, params=[('page',(currentPage*50) - 50)])
        res.raise_for_status()
        # Parse results
        topmanga_soup = BeautifulSoup(res.content, 'html.parser')
        mangaList = topmanga_soup.select('#main_content > div:nth-child(2) > div:nth-child(2) > div.col-12.col-lg-6.p-3.text')
        for manga in mangaList:
            url = mangaDiv.select('div:nth-child(2) > div > div:nth-child(1)')[0].find('a',attrs={'alt':'Series Info'})['href']
            urls.append(url)
        time.sleep(1)
    return urls

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)