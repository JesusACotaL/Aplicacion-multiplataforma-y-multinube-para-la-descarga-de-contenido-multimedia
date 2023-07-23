# This is a myAnimeList scrapper made for the purpose of searching and finding the most accurate information possible.
# Version: 1.0.2
from bs4 import BeautifulSoup
import requests

import logging
import re
import time
import csv
import base64
from urllib.error import HTTPError

def parseMangaSoup(soup, debug=False):
    """ Parses a full manga page soup into a dictionary """
    output_dict = {}

    # Original name
    name = soup.find('span', itemprop='name').find(string=True)
    output_dict['name'] = name
    if debug: print(name)

    # Original url
    mangaURL = soup.find('div', attrs={'class': 'breadcrumb','itemtype':'http://schema.org/BreadcrumbList'})
    mangaURL = mangaURL.find('meta', attrs={'content':'3'}).find_previous_sibling()
    mangaURL = mangaURL['href']
    output_dict['mangaURL'] = mangaURL
    if debug: print(mangaURL)

    # English name
    name_english = soup.find('span', string='English:')
    if(name_english):
        name_english = name_english.next_sibling.strip()
    else:
        name_english=''
    output_dict['name_english'] = name_english
    if debug: print(name_english)

    # Authors
    authors = soup.find('span', string='Authors:').find_next_sibling('a').string
    output_dict['authors'] = authors
    if debug: print(authors)

    # Date
    date = soup.find('span', string='Published:').next_sibling.strip()
    output_dict['date'] = date
    if debug: print(date)

    # Status
    status = soup.find('span', string='Status:').next_sibling.strip()
    output_dict['status'] = status
    if debug: print(status)

    # Genres
    genresDiv = soup.find_all('span', itemprop='genre')
    genres = ', '.join([g.string for g in genresDiv])
    output_dict['genres'] = genres
    if debug: print(genres)

    # Characters
    charactersDiv = soup.find(lambda tag:tag.name=="h2" and "Characters" in tag.text).next_sibling
    characters = charactersDiv.find_all(lambda tag:tag.name=="a" and tag.string != None)
    charactersList = []
    if(characters[0].string != 'here'): # Check if there are any characters
        for c in characters:
            character = {}
            # Name
            character['name']=c.string
            if debug: print(c.string)
            # Role
            character['role']=c.next_sibling.next_sibling.find('small').string
            if debug: print(c.next_sibling.next_sibling.find('small').string)
            # Image
            cImgSrc=c.parent.find_previous_sibling().a.img['data-src']
            cImgSrc = re.sub(r'r/\d+x\d+/', '', cImgSrc)
            character['image'] = cImgSrc
            if debug: print(c.parent.find_previous_sibling().a.img['data-src'])
            charactersList.append(character)
            # URL
            character['url']=c['href']
            if debug: print(c['href'])    
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
    if debug: print(score, 'by', score)
    if debug: print(score, 'by', scoreUsers)

    
    ranked = soup.find('span', string='Ranked:').next_sibling.strip()
    statistics['ranked'] = ranked
    if debug: print(ranked)
    
    popularity = soup.find('span', string='Popularity:').next_sibling.strip()
    statistics['popularity'] = popularity
    if debug: print(popularity)
    output_dict['statistics'] = statistics

    # Oficial site (if exists)
    site = soup.find(lambda tag:tag.name=="h2" and "Available At" in tag.text)
    if(site):
        site = site.next_sibling.a['href']
    if debug: print(site)
    output_dict['site'] = site

    # Synopsis
    synopsis = ''
    synopsisDiv = soup.find('span', itemprop='description')
    if(synopsisDiv):
        synopsis = synopsisDiv.text
    output_dict['synopsis'] = synopsis
    if debug: print(synopsis)

    # Background
    background = ''
    backgroundDiv = soup.find(lambda tag:tag.name=="h2" and "Background" in tag.text).next_siblings
    if(backgroundDiv):
        background = ' '.join([item.text for item in backgroundDiv])
    if debug: print(background)
    output_dict['background'] = background

    # Image
    img = soup.find('img', itemprop='image')
    output_dict['img'] = img['data-src']

    return output_dict

def scrapManga(manga_url):
    try:
        res = requests.get(manga_url)
        res.raise_for_status()
        manga_soup = BeautifulSoup(res.content, 'html.parser')
        result = parseMangaSoup(manga_soup)
        # Original myanimelist ID
        mangaID = re.findall("\/[0-9]+\/",manga_url)[0][1:-1]
        result['mangaID'] = mangaID
        return result
    except HTTPError:
        print('Couldnt scrap manga: '+str(manga_url))
        return None

def searchMangaOnline(text, debug=False):
    search_url = 'https://myanimelist.net/manga.php?cat=manga'
    res = requests.get(search_url, params=[('q',text)])
    res.raise_for_status()
    manga_soup = BeautifulSoup(res.content, 'html.parser')
    
    html = manga_soup.select('#content > div.js-categories-seasonal.js-block-list.list > table > tr')
    html = html[1:] # Delete tr title

    # Extract data from each one
    mangasFound = []
    for mangaDiv in html:
        manga = {}
        name = mangaDiv.select('td:nth-child(2) > a.hoverinfo_trigger.fw-b')[0].find('strong').text
        manga['name'] = name
        
        url = mangaDiv.select('td:nth-child(2) > a.hoverinfo_trigger.fw-b')[0]['href']
        manga['url'] = url
        
        score = mangaDiv.select('td:nth-child(5)')[0].text
        score = ''.join(e for e in score if e.isalnum() or e == '.') # Delete special char
        manga['score'] = score

        # Instead of that tiny thumbnail, we must remove any resolution parameters
        img = mangaDiv.select('td:nth-child(1)')[0].find('img')['data-src']
        img = re.sub(r'r/\d+x\d+/', '', img)
        manga['img'] = img
        
        short_desc = mangaDiv.select('td:nth-child(2)')[0].select(':nth-child(4)')[0].text
        manga['short_desc'] = short_desc

        if debug: print(title)
        if debug: print(url)
        if debug: print(score)
        if debug: print(img)
        if debug: print(short_desc)
        mangasFound.append(manga)
    return mangasFound

def testlocal():
    # Test de scrap
    manga_soup = BeautifulSoup(open('onepiece.html', encoding="utf8"), 'html.parser')
    print(parseMangaSoup(manga_soup))
    
    # Test de busqueda
    # manga_soup = BeautifulSoup(open('testBusqueda.html', encoding="utf8"), 'html.parser')
    # html = manga_soup.select('#content > div.js-categories-seasonal.js-block-list.list > table > tr')
    # html = html[1:] # Delete tr title
    # # Data
    # title = html[0].select('td:nth-child(2) > a.hoverinfo_trigger.fw-b')[0].find('strong').text
    # url = html[0].select('td:nth-child(2) > a.hoverinfo_trigger.fw-b')[0]['href']
    # score = html[0].select('td:nth-child(5)')[0].text
    # score = ''.join(e for e in score if e.isalnum() or e == '.') # Delete special char
    # img = html[0].select('td:nth-child(1)')[0].find('img')['data-src']
    # short_desc = html[0].select('td:nth-child(2)')[0].select(':nth-child(4)')[0].text
    # print(title)
    # print(url)
    # print(score)
    # print(img)
    # print(short_desc)
    pass

def getImageBase64(imageURL):
    """
    Returns a single binary image encoded in base64 format
    """
    url = imageURL
    res = requests.get(url)
    res.raise_for_status()
    binaryImage = res.content
    image_string = base64.b64encode(binaryImage) # Base64 compressed image
    return image_string

def createCSV(filename='mangas.csv'):
    """ Creates and erases csv for mangas"""
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
        time.sleep(1)
        csv_file.close()

def getTopMangas(limit, delay=1, filename='mangas.csv'):
    """ Fetches 50 top mangas, starting on number <LIMIT> and then writes the most important data in a CSV file """
    url = 'https://myanimelist.net/topmanga.php'
    res = requests.get(url, params=[('limit',limit)])
    res.raise_for_status()
    topmanga_soup = BeautifulSoup(res.content, 'html.parser')
    topmanga_soupTable = topmanga_soup.find('table', attrs={'class':'top-ranking-table'})
    mangaList = topmanga_soupTable.find_all('tr', attrs={'class':'ranking-list'})
    mangasInfo = []
    for manga in mangaList:
        mangaURL = manga.find('td', attrs={'class':'title al va-t clearfix word-break'}).findChildren('a')
        mangaURL = mangaURL[0]['href']
        print(mangaURL)
        mangaInfo = scrapManga(mangaURL)
        if(mangaInfo):
            mangasInfo.append(mangaInfo)
        time.sleep(delay)
    for manga in mangasInfo:
        csvWriter(manga, filename=filename)
    print(mangasInfo)

def getMangasByID(amount, delay=1):
    """ Fetches a bunch of manga based on IDs, and then writes the most important data in a CSV file """
    mangaURL = 'https://myanimelist.net/manga/'
    mangaID = 1
    mangasInfo = []
    while mangaID < amount:
        url = mangaURL+str(mangaID)
        print(url)
        mangaInfo = scrapManga(url)
        if(mangaInfo):
            mangasInfo.append(mangaInfo)
        mangaID = mangaID + 1
        time.sleep(delay)
    for manga in mangasInfo:
        csvWriter(manga)
    print(mangasInfo)

if __name__ == '__main__':
    #testlocal()
    createCSV(filename='mangas2.csv')
    getTopMangas(50,filename='mangas2.csv')