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

siteURL = "https://ww5.mangakakalot.tv"

# Initialize browser configurations
from selenium import webdriver # Javascript support
from selenium.webdriver.chrome.options import Options # Browser headless option
browserConfig = Options()
browserConfig.add_argument('--headless')
browserConfig.add_argument('--no-sandbox')
browserConfig.add_argument("--log-level=3") # Hide debug info that we dont care about
browserConfig.add_experimental_option('excludeSwitches', ['enable-logging']) # Hide chromedriver debug info
browserConfig.add_argument('--disable-dev-shm-usage')

# Stuff to make chromdriver cli window dissapear in selenium4
from selenium.webdriver.chrome.service import Service
# Only works in windows from subprocess import CREATE_NO_WINDOW

def renderWithJavascript(url, classToBeFound=None):
    browserService = Service()
    # Only works in windows browserService.creation_flags = CREATE_NO_WINDOW
    browser = webdriver.Chrome(options=browserConfig,service=browserService)
    browser.get(url)
    # Wait for element to be rendered
    # More info https://www.selenium.dev/documentation/webdriver/waits/
    try:
        WebDriverWait(browser, timeout=2).until(lambda d: d.find_element(By.CLASS_NAME,classToBeFound))
    except:
        pass
    html = browser.page_source
    browser.close()
    return html

@app.route("/")
def info():
    return "<p>mangakakalot.tv Scrapper v1</p>"

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
    # Purify search query
    searchQuery = urllib.parse.quote(searchQuery)
    url = siteURL+"/search/"+searchQuery
    # Render w/ javascript
    html = renderWithJavascript(url, 'panel_story_list')
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
    # Render w/ javascript
    html = renderWithJavascript(mangaURL, 'chapter-list')
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
    # Render w/ javascript
    html = renderWithJavascript(chapterURL, 'img-loading')
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find('div',attrs={'id':'vungdoc'}).find_all('img',attrs={'class':'img-loading', 'data-src':True})
    links = []
    for link in resultHTML:
        newlink = link['data-src']
        links.append(newlink)
    return links

@app.post("/getImageBlob")
def getImageBlob():
    """
    Parameters: url
    Returns a single binary image
    """
    data = request.json
    url = data['url']
    res = requests.get(url, headers={'referer': siteURL})
    res.raise_for_status()
    imgBlob = res.content
    buffer = io.BytesIO(imgBlob)
    response = send_file(buffer, mimetype='image/jpeg')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)