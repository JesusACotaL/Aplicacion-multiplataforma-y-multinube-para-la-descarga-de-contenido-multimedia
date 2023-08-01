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
    return "<p>myAnimeList Scrapper v1</p>"

@app.post("/searchManga")
def searchManga():
    """
    Parameters: manga, safeSearch(boolean)
    Returns an array[] like:
    [
        {
            "name": ""
            "img": "",
            "short_desc": "",
            "url": "",
            "mangaType": "",
            "chapAmount": "",
            "score": "",
        }
    ]
    """
    data = request.json
    searchQuery = data['manga']
    safeSearch = data['safeSearch']

    # Get HTML
    siteUrl = "https://myanimelist.net/manga.php"
    columns = ['a', 'g', 'c', 'f'] # Type=a, Chapters=c, Score=g, ,Total members=f
    excluded_genres = []
    if(safeSearch == "true"):
        excluded_genres = [49, 12] # Exclude Erotica and Hentai
    parameters = {
        'cat': 'manga',
        'q' : searchQuery,
        'type' : 0,
        'score' : 0,
        'status' : 0,
        'mid' : 0,
        'sm' : 0,
        'sd' : 0,
        'sy' : 0,
        'em' : 0,
        'ed' : 0,
        'ey' : 0,
        'c[]' : columns,
        'genre_ex[]' : excluded_genres
    }
    encodedParams = urllib.parse.urlencode(parameters, doseq=True)
    search_url = 'https://myanimelist.net/manga.php?%s' % encodedParams
    res = requests.get(search_url)
    res.raise_for_status()
    manga_soup = BeautifulSoup(res.content, 'html.parser')
    html = manga_soup.select('#content > div.js-categories-seasonal.js-block-list.list > table > tr')
    html = html[1:] # Delete tr title

    # Extract data from each one
    mangasFound = []
    for mangaDiv in html:
        manga = {}

        img = ''
        img = mangaDiv.select('td:nth-child(1)')[0].find('img')['data-src']
        img = re.sub(r'r/\d+x\d+/', '', img) # Instead of that tiny thumbnail, we must remove any resolution parameters
        manga['img'] = img

        name = ''
        name = mangaDiv.select('td:nth-child(2) > a.hoverinfo_trigger.fw-b')[0].find('strong').string
        name = name.strip('\r\n').lstrip(' \r\n').rstrip(' \r\n')
        manga['name'] = name
        
        short_desc = ''
        short_desc = mangaDiv.select('td:nth-child(2)')[0].select(':nth-child(4)')[0].text
        short_desc = short_desc.strip('\r\n').lstrip(' \r\n').rstrip(' \r\n')
        manga['short_desc'] = short_desc

        url = ''
        url = mangaDiv.select('td:nth-child(2) > a.hoverinfo_trigger.fw-b')[0]['href']
        manga['url'] = url

        mangaType = ''
        mangaType = mangaDiv.select('td:nth-child(3)')[0].string
        mangaType = mangaType.strip('\r\n').lstrip(' \r\n').rstrip(' \r\n')
        manga['mangaType'] = mangaType
        
        chapAmount = ''
        chapAmount = mangaDiv.select('td:nth-child(4)')[0].string
        chapAmount = chapAmount.strip('\r\n').lstrip(' \r\n').rstrip(' \r\n')
        chapAmount = '' if chapAmount == '-' else chapAmount
        manga['chapAmount'] = chapAmount
        
        score = ''
        score = mangaDiv.select('td:nth-child(5)')[0].string
        score = score.strip('\r\n').lstrip(' \r\n').rstrip(' \r\n')
        manga['score'] = score

        mangasFound.append(manga)
    return mangasFound

@app.post("/getMangaInfo")
def getMangaInfo():
    """
    Parameters: url
    Returns an object like:
    {
        "name": ""
        "mangaURL": "",
        "name_english": "",
        "authors": "",
        "date": "",
        "status": "",
        "genres": "",
        "characters": [
            {
                "name": "",
                "role": "",
                "image": "",
                "url": "",
            }
        ],
        "statistics": [
            {
                "score": "",
                "scoreUsers": "",
                "ranked": "",
                "popularity": "",
            }
        ],
        "site": "",
        "synopsis": "",
        "background": "",
        "img": "",
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
    name = html.find('span', itemprop='name').find(string=True)
    manga['name'] = name

    # Original url
    mangaURL = html.find('div', attrs={'class': 'breadcrumb','itemtype':'http://schema.org/BreadcrumbList'})
    mangaURL = mangaURL.find('meta', attrs={'content':'3'}).find_previous_sibling()
    mangaURL = mangaURL['href']
    manga['mangaURL'] = mangaURL

    # Original myanimelist ID
    mangaID = re.findall("\/[0-9]+\/",mangaURL)[0][1:-1]
    manga['mangaID'] = mangaID

    # English name
    name_english = html.find('span', string='English:')
    if(name_english):
        name_english = name_english.next_sibling.strip()
    else:
        name_english=''
    manga['name_english'] = name_english

    # Authors
    authors = html.find('span', string='Authors:').find_next_sibling('a').string
    manga['authors'] = authors

    # Date
    date = html.find('span', string='Published:').next_sibling.strip()
    manga['date'] = date

    # Status
    status = html.find('span', string='Status:').next_sibling.strip()
    manga['status'] = status

    # Genres
    genresDiv = html.find_all('span', itemprop='genre')
    genres = ', '.join([g.string for g in genresDiv])
    manga['genres'] = genres

    # Characters
    charactersDiv = html.find(lambda tag:tag.name=="h2" and "Characters" in tag.text).next_sibling
    characters = charactersDiv.find_all(lambda tag:tag.name=="a" and tag.string != None)
    charactersList = []
    if(characters[0].string != 'here'): # Check if there are any characters
        for c in characters:
            character = {}
            # Name
            character['name']=c.string
    
            # Role
            character['role']=c.next_sibling.next_sibling.find('small').string
    
            # Image
            cImgSrc=c.parent.find_previous_sibling().a.img['data-src']
            cImgSrc = re.sub(r'r/\d+x\d+/', '', cImgSrc)
            character['image'] = cImgSrc
    
            charactersList.append(character)
            # URL
            character['url']=c['href']
    
    manga['characters'] = charactersList
    
    # Statistics
    statistics = {}
    scoreDiv = html.find('span', string='Score:').find_next_sibling('span').span
    score = 'N/A'
    scoreUsers = 'N/A'
    if(not scoreDiv.find(string="N/A")):
        score = html.find('span', string='Score:').find_next_sibling('span').span.string
        scoreUsers = html.find('span', string='Score:').find_next_sibling('span').find(itemprop='ratingCount').string
    statistics['score'] = score
    statistics['scoreUsers'] = scoreUsers

    
    ranked = html.find('span', string='Ranked:').next_sibling.strip()
    statistics['ranked'] = ranked
    
    popularity = html.find('span', string='Popularity:').next_sibling.strip()
    statistics['popularity'] = popularity
    manga['statistics'] = statistics

    # Oficial site (if exists)
    site = html.find(lambda tag:tag.name=="h2" and "Available At" in tag.text)
    if(site):
        site = site.next_sibling.a['href']
    manga['site'] = site

    # Synopsis
    synopsis = ''
    synopsisDiv = html.find('span', itemprop='description')
    if(synopsisDiv):
        synopsis = synopsisDiv.text
        synopsis = ''.join(e for e in synopsis if e.isalnum() or e == '/' or e == '_' or e == ':' or e == ' ' or e == '.' or e == ',')
        synopsis = synopsis.strip(' \n\r')
    manga['synopsis'] = synopsis

    # Background
    background = ''
    backgroundDiv = html.find(lambda tag:tag.name=="h2" and "Background" in tag.text).next_siblings
    if(backgroundDiv):
        background = ' '.join([item.text for item in backgroundDiv])
        background = ''.join(e for e in background if e.isalnum() or e == '/' or e == '_' or e == ':' or e == ' ' or e == '.' or e == ',')
        background = background.strip(' \n\r')
    manga['background'] = background

    # Image
    img = html.find('img', itemprop='image')
    manga['img'] = img['data-src']

    return manga

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)