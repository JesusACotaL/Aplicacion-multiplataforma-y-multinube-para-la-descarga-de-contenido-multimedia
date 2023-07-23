import re
import json
import io

import requests

scrapperManganeloAPI = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/si"

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
    searchQuery = re.sub(r'\ ','_',searchQuery) # replace whitespaces with underscores
    searchQuery = ''.join(e for e in searchQuery if e.isalnum() or e == '/' or e == '_' or e == ':') # remove weird characters
    searchQuery = searchQuery.lower() # uncapitalize
    body = {"url": "https://m.manganelo.com/search/story/"+searchQuery}
    res = requests.post(scrapperManganeloAPI+"/get-manga-info", json=body)
    res.raise_for_status()
    return json.loads(res.content)

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
    body = {"url": mangaURL}
    res = requests.post(scrapperManganeloAPI+"/get-manga-chapters", json=body)
    res.raise_for_status()
    results = json.loads(res.content)['search_items']
    results.reverse() # Reverse because site goes lastest-first
    return results

def getChapterURLS(chapterURL):
    """
    Returns an array[] like:
    [
        "url": ""
    ]
    """
    body = {"url": chapterURL}
    res = requests.post(scrapperManganeloAPI+"/get-manga-urls", json=body)
    res.raise_for_status()
    return json.loads(res.content)

def getImageBlob(imageURL):
    """
    Returns a single binary image
    """
    url = imageURL
    res = requests.get(url, headers={'referer': 'https://chapmanganelo.com/'})
    res.raise_for_status()    
    imgBlob = res.content
    return imgBlob