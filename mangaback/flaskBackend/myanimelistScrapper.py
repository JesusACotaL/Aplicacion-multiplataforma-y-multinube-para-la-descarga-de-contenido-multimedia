# This is a myAnimeList scrapper made for the purpose of searching and finding the most accurate information possible.
# Version: 1.0.2
from bs4 import BeautifulSoup
import requests

import logging
import re
import time
import csv
import urllib

def parseMangaSoup(soup):
    """ Parses a full manga page soup into a dictionary """
    output_dict = {}

    # Original name
    name = soup.find('span', itemprop='name').find(string=True)
    output_dict['name'] = name

    # Original url
    mangaURL = soup.find('div', attrs={'class': 'breadcrumb','itemtype':'http://schema.org/BreadcrumbList'})
    mangaURL = mangaURL.find('meta', attrs={'content':'3'}).find_previous_sibling()
    mangaURL = mangaURL['href']
    output_dict['mangaURL'] = mangaURL

    # English name
    name_english = soup.find('span', string='English:')
    if(name_english):
        name_english = name_english.next_sibling.strip()
    else:
        name_english=''
    output_dict['name_english'] = name_english

    # Authors
    authors = soup.find('span', string='Authors:').find_next_sibling('a').string
    output_dict['authors'] = authors

    # Date
    date = soup.find('span', string='Published:').next_sibling.strip()
    output_dict['date'] = date

    # Status
    status = soup.find('span', string='Status:').next_sibling.strip()
    output_dict['status'] = status

    # Genres
    genresDiv = soup.find_all('span', itemprop='genre')
    genres = ', '.join([g.string for g in genresDiv])
    output_dict['genres'] = genres

    # Characters
    charactersDiv = soup.find(lambda tag:tag.name=="h2" and "Characters" in tag.text).next_sibling
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
    
    output_dict['characters'] = charactersList
    
    # Statistics
    statistics = {}
    scoreDiv = soup.find('span', string='Score:').find_next_sibling('span').span
    score = 'N/A'
    scoreUsers = 'N/A'
    if(not scoreDiv.find(string="N/A")):
        score = soup.find('span', string='Score:').find_next_sibling('span').span.string
        scoreUsers = soup.find('span', string='Score:').find_next_sibling('span').find(itemprop='ratingCount').string
    statistics['score'] = score
    statistics['scoreUsers'] = scoreUsers

    
    ranked = soup.find('span', string='Ranked:').next_sibling.strip()
    statistics['ranked'] = ranked
    
    popularity = soup.find('span', string='Popularity:').next_sibling.strip()
    statistics['popularity'] = popularity
    output_dict['statistics'] = statistics

    # Oficial site (if exists)
    site = soup.find(lambda tag:tag.name=="h2" and "Available At" in tag.text)
    if(site):
        site = site.next_sibling.a['href']
    output_dict['site'] = site

    # Synopsis
    synopsis = ''
    synopsisDiv = soup.find('span', itemprop='description')
    if(synopsisDiv):
        synopsis = synopsisDiv.text
    output_dict['synopsis'] = synopsis

    # Background
    background = ''
    backgroundDiv = soup.find(lambda tag:tag.name=="h2" and "Background" in tag.text).next_siblings
    if(backgroundDiv):
        background = ' '.join([item.text for item in backgroundDiv])
    output_dict['background'] = background

    # Image
    img = soup.find('img', itemprop='image')
    output_dict['img'] = img['data-src']

    return output_dict

def scrapManga(manga_url):
    manga = {}
    try:
        res = requests.get(manga_url)
        res.raise_for_status()
        manga_soup = BeautifulSoup(res.content, 'html.parser')
        manga = parseMangaSoup(manga_soup)
        # Original myanimelist ID
        mangaID = re.findall("\/[0-9]+\/",manga_url)[0][1:-1]
        manga['mangaID'] = mangaID
    except requests.exceptions.HTTPError:
        print('Couldnt scrap manga: '+str(manga_url))
    return manga

def searchMangaOnline(text, safeSearch=False):
    siteUrl = "https://myanimelist.net/manga.php"
    # Type=a, Chapters=c, Score=g, ,Total members=f
    columns = ['a', 'g', 'c', 'f'] 
    excluded_genres = []
    if(safeSearch):
        excluded_genres = [49, 12] # Exclue Erotica and Hentai
    parameters = {
        'cat': 'manga',
        'q' : text,
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

def getImageBlob(imageURL):
    """
    Returns a single binary image
    """
    url = imageURL
    res = requests.get(url)
    res.raise_for_status()
    binaryImage = res.content
    return binaryImage

def createCSV(filename='mangas.csv'):
    """ Creates / Cleans CSV with headers for mangas"""
    fieldnames = ['mangaID', 'name', 'genres', 'authors', 'img', 'mangaURL']
    with open(filename, 'w', encoding="utf-8", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        csv_file.close()

def csvWriter(manga, filename='mangas.csv'):
    """ Writes the most important data of a manga dictionary in a CSV file """
    fieldnames = ['mangaID', 'name', 'genres', 'authors', 'img', 'mangaURL']
    del manga['synopsis']
    del manga['background']
    del manga['name_english']
    del manga['site']
    del manga['statistics']
    del manga['characters']
    del manga['status']
    del manga['date']
    with open(filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(manga)
        csv_file.close()

def getTopMangasToCSV(limit, delay=1, filename='mangas.csv'):
    """ Fetches 50 top mangas and then writes the most important data in a CSV file """
    currentMangaID = 1
    createCSV(filename=filename)
    currentPage = 1
    pageAmount = limit / 50
    while(currentPage < pageAmount):
        # Request search
        url = 'https://myanimelist.net/topmanga.php'
        res = requests.get(url, params=[('limit',(currentPage*50) - 50)])
        res.raise_for_status()
        html = res.content
        # Parse results
        topmanga_soup = BeautifulSoup(html, 'html.parser')
        topmanga_soupTable = topmanga_soup.find('table', attrs={'class':'top-ranking-table'})
        mangaList = topmanga_soupTable.find_all('tr', attrs={'class':'ranking-list'})
        for manga in mangaList:
            mangaURL = manga.find('td', attrs={'class':'title al va-t clearfix word-break'}).findChildren('a')
            mangaURL = mangaURL[0]['href']
            mangaInfo = scrapManga(mangaURL)
            mangaInfo['mangaID'] = currentMangaID
            csvWriter(mangaInfo, filename=filename)
            print('Scrapped: '+mangaURL)
            currentMangaID = currentMangaID + 1
            time.sleep(delay)
        currentPage = currentPage + 1

if __name__ == '__main__':
    #print(searchMangaOnline('boku no pico')[0])
    getTopMangasToCSV(200, delay=1,filename='test.csv')