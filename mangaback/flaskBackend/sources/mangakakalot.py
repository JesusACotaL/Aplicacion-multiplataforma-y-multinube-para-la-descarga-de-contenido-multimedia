import re
import json
import base64
import io

import requests
from PIL import Image
from bs4 import BeautifulSoup

from selenium import webdriver # Javascript support
from selenium.webdriver.chrome.options import Options # Browser headless option
import urllib

siteURL = "https://ww5.mangakakalot.tv"

def renderWithJavascript(url):
    # Headless configuration
    browserConfig = Options()
    browserConfig.add_argument('-headless')
    browser = webdriver.Chrome(options=browserConfig)
    browser.get(url)
    html = browser.page_source
    browser.close()
    return html

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
    html = renderWithJavascript(url)
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
    html = renderWithJavascript(mangaURL)
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
    html = renderWithJavascript(chapterURL)
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find('div',attrs={'id':'vungdoc'}).find_all('img',attrs={'class':'img-loading', 'data-src':True})
    links = []
    for link in resultHTML:
        newlink = link['data-src']
        links.append(newlink)
    links.reverse() # Reverse because site goes lastest-first
    return links

def getImageBase64(imageURL):
    """
    Returns a single binary image encoded in base64 format
    """
    url = imageURL
    res = requests.get(url, headers={'referer': siteURL})
    res.raise_for_status()
    # Compress image
    binaryImage = res.content
    im_file = io.BytesIO(binaryImage) # File-like object
    imgPIL = Image.open(im_file) # PIL image
    buffer = io.BytesIO() # Memory for compression operations

    # Save image as JPEG format, and apply image compression, number must be in %
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg-saving
    imgPIL.save(buffer,format='JPEG',optimize=True,quality=50)
    
    imgBinaryCompressed = buffer.getvalue()
    image_string = base64.b64encode(imgBinaryCompressed) # Base64 compressed image
    return image_string

if __name__ == '__main__':
    #res = searchManga('pokemon')
    #print(res[0])
    res = getMangaChapters('https://ww5.mangakakalot.tv/manga/manga-ok991667')
    print(res[0])
    #res = getChapterURLS('https://ww5.mangakakalot.tv/chapter/manga-ok991667/chapter-1')
    #print(res)
    #res = getImageBase64('https://cm.blazefast.co/62/1b/621b3c68e968efd37d2cb5c37d61060d.jpg')