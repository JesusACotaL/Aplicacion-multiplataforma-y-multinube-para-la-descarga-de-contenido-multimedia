import re
import json
import io
import time

import requests
from bs4 import BeautifulSoup

import urllib

siteURL = "https://mangakakalot.com/"

# Initialize browser so we dont delay requests
from selenium import webdriver # Javascript support
from selenium.webdriver.chrome.options import Options # Browser headless option
browserConfig = Options()
browserConfig.add_argument('-headless')
browserConfig.add_argument("--log-level=3") # Hide debug info that we dont care about
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
    searchQuery = re.sub(r'\ ','_',searchQuery) # replace whitespaces with underscores
    searchQuery = searchQuery.lower() # uncapitalize
    searchQuery = urllib.parse.quote(searchQuery)
    url = siteURL+"/search/story/"+searchQuery
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
        newmanga['chapters_url'] = manga.find('h3',attrs={'class':'story_name'}).find('a')['href']
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
    resultHTML = manga_soup.find('div',attrs={'class':'panel-story-chapter-list'}).find_all('li',attrs={'class':'a-h'})
    chapters = []
    for chapter in resultHTML:
        newchapter = {}
        name = chapter.find('a').string
        # remove weird characters and whitelines at beginning
        name = ''.join(e for e in name if e.isalnum() or e == '/' or e == '_' or e == ':' or e == ' ')
        name = name.lstrip(' ')
        newchapter['name'] = name
        newchapter['url'] = chapter.find('a')['href']
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
    resultHTML = manga_soup.find('div', attrs={'class':'container-chapter-reader'}).find_all('img',attrs={'src':True})
    links = []
    for link in resultHTML:
        newlink = link['src']
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
    res = searchManga('One Piece')
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