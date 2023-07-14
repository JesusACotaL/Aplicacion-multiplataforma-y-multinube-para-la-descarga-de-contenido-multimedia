import re
import json
import base64

import requests
scrapperManganeloAPI = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/si"

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
def searchManga(searchQuery):
    searchQuery = re.sub(r'\ ','_',searchQuery) # replace whitespaces with underscores
    searchQuery = ''.join(e for e in searchQuery if e.isalnum() or e == '/' or e == '_' or e == ':') # remove weird characters
    searchQuery = searchQuery.lower() # uncapitalize
    body = {"url": "https://m.manganelo.com/search/story/"+searchQuery}
    res = requests.post(scrapperManganeloAPI+"/get-manga-info", json=body)
    res.raise_for_status()
    return json.loads(res.content)

"""
Returns an array[] like:
[
	{
		"name": "",
		"url": ""
	}
]
"""
def getMangaChapters(mangaURL):
    body = {"url": mangaURL}
    res = requests.post(scrapperManganeloAPI+"/get-manga-chapters", json=body)
    res.raise_for_status()
    results = json.loads(res.content)['search_items']
    return results

"""
Returns an array[] like:
[
	{
		"url": ""
	}
]
"""
def getChapterURLS(chapterURL):
    body = {"url": chapterURL}
    res = requests.post(scrapperManganeloAPI+"/get-manga-urls", json=body)
    res.raise_for_status()
    return json.loads(res.content)

"""
Returns a single binary image encoded in base64 format
"""
def getImageBase64(imageURL):
    url = imageURL
    res = requests.get(url, headers={'referer': 'https://chapmanganelo.com/'})
    res.raise_for_status()
    image_string = base64.b64encode(res.content)
    return image_string