"""
Turns out mangadex is not actually a site to watch manga, but rather a front end for 
the real site called https://mangaplus.shueisha.co.jp/
So, this scrapper is useless
But it contains several useful functions so im leaving it here.

1. It contains code to set and retrieve localStorage on the browser.
2. It contains code to force the browser to wait until javascript is loaded.
3. It contains code that examples why using window.URL can make images unscrappable, because they are deleted after usage
"""
import re
import json
import io

import requests
from PIL import Image
from bs4 import BeautifulSoup
import urllib

siteURL = "https://mangadex.org"
dataConfig = {"metadata":{"version":0,"modified":1690095946467},"readingHistory":{"_readingHistory":[["2a70572c-e0ab-4930-bf68-fdd5b87ffdfb","2023-06-20T23:23:55.307Z"],["ddffda9a-c15c-4e42-ac09-adaefb97965b","2023-02-12T01:53:23.601Z"]]},"userPreferences":{"filteredLanguages":["en"],"originLanguages":[],"paginationCount":100,"listMultiplier":3,"showSafe":True,"showErotic":True,"showSuggestive":True,"showHentai":False,"theme":"system","mdahPort443":False,"dataSaver":False,"groupBlacklist":[],"userBlacklist":[],"locale":"en","interfaceLocale":"en"}}

# Initialize browser so we dont delay requests
from selenium import webdriver # Javascript support
from selenium.webdriver.chrome.options import Options # Browser headless option
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
browserConfig = Options()
browserConfig.add_argument('-headless')
browser = webdriver.Chrome(options=browserConfig)
browser.get('https://www.google.com')

def renderWithJavascript(url, classToBeFound=None):
    # Prepare site with configurations
    browser.get(siteURL)
    # Set preferences for mangadex browser
    value = json.dumps(dataConfig)
    browser.execute_script('window.localStorage.setItem("md",arguments[0])',value)

    # Load requested page
    browser.get(url)
    # Wait for element to be rendered, or just wait
    # More info https://www.selenium.dev/documentation/webdriver/waits/
    try:
        WebDriverWait(browser, timeout=2).until(lambda d: d.find_element(By.CLASS_NAME,classToBeFound))
    except:
        pass

    localStorage = browser.execute_script('return window.localStorage.getItem("md")')
    #print(localStorage)
    
    html = browser.page_source
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
    url = siteURL+"/search?q="+searchQuery
    # Render w/ javascript
    html = renderWithJavascript(url, classToBeFound='manga-card-dense')
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find_all('a',attrs={'class':'manga-card-dense'})
    mangas = []
    for manga in resultHTML:
        newmanga = {}
        newmanga['name'] = manga.find('a',attrs={'class':'font-bold title'}).find('span').string
        newmanga['chapters_url'] = siteURL + manga['href'] + '?order=asc'
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
    html = renderWithJavascript(mangaURL, classToBeFound='chapter-grid flex-grow')
    # Parse HTML into dictionary
    manga_soup = BeautifulSoup(html, 'html.parser')
    resultHTML = manga_soup.find_all('div',attrs={'class':'chapter-grid flex-grow'})
    chapters = []
    for chapter in resultHTML:
        newchapter = {}
        newchapter['name'] = chapter.find_all('a')[0]['title']
        newchapter['url'] = chapter.find_all('a')[0]['href']
        print(newchapter)
        chapters.append(newchapter)
    chapters.reverse() # Reverse because site goes lastest-first
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
        WebDriverWait(browser, timeout=2).until(lambda d: d.find_element(By.CLASS_NAME,'zao-image'))
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
    return imageURL
    # url = imageURL
    # res = requests.get(url)
    # res.raise_for_status()
    # # Compress image
    # binaryImage = res.content
    # im_file = io.BytesIO(binaryImage) # File-like object
    # imgPIL = Image.open(im_file) # PIL image
    # buffer = io.BytesIO() # Memory for compression operations

    # # Save image as JPEG format, and apply image compression, number must be in %
    # # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg-saving
    # imgPIL.save(buffer,format='JPEG',optimize=True,quality=50)
    
    # imgBinaryCompressed = buffer.getvalue()
    # return imgBinaryCompressed

if __name__ == '__main__':
    #res = searchManga('pokemon')
    #print(res[0])
    #res = getMangaChapters('https://mangadex.org/title/a1c7c817-4e59-43b7-9365-09675a149a6f/one-piece?order=asc')
    #print(res[0])
    res = getChapterURLS('https://mangaplus.shueisha.co.jp/viewer/1000486')
    print(res)