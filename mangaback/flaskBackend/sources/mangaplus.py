import re
import json
import io
import time

import requests
from bs4 import BeautifulSoup
import urllib

siteURL = "https://mangaplus.shueisha.co.jp"

# Initialize browser so we dont delay requests
from selenium import webdriver # Javascript support
from selenium.webdriver.chrome.options import Options # Browser headless option
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
browserConfig = Options()
browserConfig.add_argument('-headless')
browserConfig.add_argument('--window-size=800x1200') # Set image resolution to capture
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
    url = siteURL+"/search_result?keyword="+searchQuery
    # Render w/ javascript
    browser.get(url)
    try:
        WebDriverWait(browser, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR,"#app > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(3)"))
    except:
        pass
    html = browser.page_source
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.select("#app > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(3) > a")
    mangas = []
    for manga in resultHTML:
        newmanga = {}
        newmanga['name'] = manga.find_all('p')[0].string
        newmanga['chapters_url'] = siteURL + manga['href']
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
    cssSelector = "#app > div:nth-child(2) > div > div:nth-child(2) > div > div > div:nth-child(2) > main > div > div:nth-child(3)"
    try:
        WebDriverWait(browser, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR,cssSelector))
    except:
        pass
    html = browser.page_source
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.select("#app > div:nth-child(2) > div > div:nth-child(2) > div > div > div:nth-child(2) > main > div > div.ChapterListItem-module_chapterListItem_ykICp")
    chapters = []
    for chapter in resultHTML:
        newchapter = {}
        newchapter['name'] = chapter.find_all('p')[1].string
        cUrl = chapter.find_all('a')[0]['href']
        idViewer = ''.join(e for e in cUrl if e.isnumeric())
        newchapter['url'] = siteURL + "/viewer/" + idViewer
        chapters.append(newchapter)
    return chapters

def getChapterURLS(chapterURL):
    """
    Returns an array[] like:
    [
        "url"
    ]
    """
    # Render w/ javascript
    browser.get(chapterURL)
    try:
        # Accept cookies if prompted
        WebDriverWait(browser, timeout=10).until(lambda d: d.find_element(By.ID,"onetrust-accept-btn-handler"))
        browser.find_element(By.ID,"onetrust-accept-btn-handler").click()
    except:
        pass
    try:
        # Wait for prompt to dissapear
        WebDriverWait(browser, timeout=10).until_not(lambda d: d.find_element(By.ID,"onetrust-accept-btn-handler"))
    except:
        pass
    # Retrieve capture of every single manga image and store it
    links = []
    images = browser.find_elements(By.CSS_SELECTOR, "img.zao-image")
    imgID = 0
    for image in images:
        filename = 'manga'+str(imgID)+'.png'
        image.screenshot('temp/'+filename)
        links.append(filename)
        imgID = imgID + 1
    return links

def getImageBlob(imageURL):
    """
    Returns a single binary image
    """
    image = None
    with open('temp/'+imageURL, 'rb')  as f:
        image = f.read()
    f.close()
    return image

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