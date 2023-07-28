import re
import json
import io
import time

import requests
from bs4 import BeautifulSoup

import urllib

siteURL = "https://ww5.mangakakalot.tv"

# Initialize browser so we dont delay requests
from selenium import webdriver # Javascript support
from selenium.webdriver.chrome.options import Options # Browser headless option
browserConfig = Options()
browserConfig.add_argument('-headless')
browser = webdriver.Chrome(options=browserConfig)

def searchManga(searchQuery):
    """
    Returns an array[] like:
    [
        {
            "name": ""
            "chapters_url": "",
            "image_url": "",
        }
    ]
    """
    # Purify search query
    searchQuery = urllib.parse.quote(searchQuery)
    url = siteURL+"/search/"+searchQuery
    # Render w/ javascript
    browser.get(url)
    html = browser.page_source
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find('div',attrs={'class':'panel_story_list'}).find_all('div',attrs={'class':'story_item'})
    mangas = []
    for manga in resultHTML:
        newmanga = {}
        newmanga['name'] = manga.find('h3',attrs={'class':'story_name'}).find('a').string
        newmanga['chapters_url'] = siteURL + manga.find('h3',attrs={'class':'story_name'}).find('a')['href']
        newmanga['image_url'] = manga.find('img')['src']
        mangas.append(newmanga)
    return mangas

def getMangaChapters(mangaURL):
    """
    Returns an array[] like:
    [
        {
            "name": "",
            "url": ""
        }
    ]
    """
    # Render w/ javascript
    browser.get(mangaURL)
    html = browser.page_source
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find('div',attrs={'class':'chapter-list'}).find_all('div',attrs={'class':'row'})
    chapters = []
    for chapter in resultHTML:
        newchapter = {}
        name = chapter.find('a').string
        # remove weird characters and whitelines at beginning
        name = ''.join(e for e in name if e.isalnum() or e == '/' or e == '_' or e == ':' or e == ' ')
        name = name.lstrip(' ')
        newchapter['name'] = name
        newchapter['url'] = siteURL + chapter.find('a')['href']
        chapters.append(newchapter)
    chapters.reverse() # Reverse because site goes lastest-first
    return chapters

def getChapterURLS(chapterURL):
    """
    Returns an array[] like:
    [
        "url": ""
    ]
    """
    # Render w/ javascript
    browser.get(chapterURL)
    html = browser.page_source
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find('div',attrs={'id':'vungdoc'}).find_all('img',attrs={'class':'img-loading', 'data-src':True})
    links = []
    for link in resultHTML:
        newlink = link['data-src']
        links.append(newlink)
    return links

def getImageBlob(imageURL):
    """
    Returns a single binary image
    """
    url = imageURL
    res = requests.get(url, headers={'referer': siteURL})
    res.raise_for_status()
    imgBlob = res.content
    return imgBlob

if __name__ == '__main__':
    res = searchManga('boku')
    print(res)
    time.sleep(1)
    res = getMangaChapters(res[0]['chapters_url'])
    print(res)
    time.sleep(1)
    res = getChapterURLS(res[0]['url'])
    print(res)
    time.sleep(1)
    getImageBlob(res[0])
    print(res)