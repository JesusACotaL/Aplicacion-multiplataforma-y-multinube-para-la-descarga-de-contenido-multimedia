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
from selenium.webdriver.edge.options import Options # Browser headless option
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
browserConfig = Options()
browserConfig.add_argument('-headless')
browser = webdriver.Edge(options=browserConfig)

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
    browser.get(chapterURL)
    try:
        WebDriverWait(browser, timeout=2).until(lambda d: d.find_element(By.CSS_SELECTOR,
        "#app > div:nth-child(2) > div > div:nth-child(2) > div > div > div:nth-child(2) > main > div > div:nth-child(3)"))
    except:
        pass
    html = browser.page_source
    
    # Parse HTML into dictionary to obtain links
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find_all('img',attrs={'class':'zao-image'})
    links = []
    for link in resultHTML:
        newlink = link['src']
        links.append(newlink)
    links.reverse() # Reverse because site goes lastest-first

    def get_file_content_chrome(driver, uri):
        # result = driver.execute_async_script("""
        #     var uri = arguments[0];
        #     var callback = arguments[1];
        #     var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        #     var xhr = new XMLHttpRequest();
        #     xhr.responseType = 'arraybuffer';
        #     xhr.onload = function(){ callback(toBase64(xhr.response)) };
        #     xhr.onerror = function(){ callback(xhr.status) };
        #     xhr.open('GET', uri);
        #     xhr.send();
        #     """, uri)
        # print(uri)
        # print(result)
        result = driver.execute_script("""
        var reader = new FileReader();
        reader.readAsArrayBuffer(blob);
        """)
        if type(result) == int :
            raise Exception("Request failed with status %s" % result)
        return result
    blob64Array = []
    for link in links:
        browser.get(link)
        try:
            WebDriverWait(browser, timeout=2).until(lambda d: False)
        except:
            pass
        blob64 = get_file_content_chrome(browser, link)
        blob64Array.append(blob64)
    return blob64Array

def getImageBlob(imageURL):
    """
    Returns a single binary image
    """
    url = imageURL
    res = requests.get(url)
    res.raise_for_status()
    imgBlob = res.content
    return imgBlob

def testSource():
    # Test to see if source works correctly
    print("Testing source, please wait...")
    print("Testing: searchManga")
    res = searchManga('boku')
    time.sleep(1)
    print("Testing: getMangaChapters")
    res = getMangaChapters(res[0]['chapters_url'])
    time.sleep(1)
    print("Testing: getChapterURLS")
    res = getChapterURLS(res[0]['url'])
    time.sleep(1)
    print("Testing: getImageBlob")
    getImageBlob(res[0])
    time.sleep(1)
    print("...success!")

if __name__ == '__main__':
    #res = searchManga('my hero')
    #print(res[0])
    res = getMangaChapters("https://mangaplus.shueisha.co.jp/titles/200019")
    print(res[0])