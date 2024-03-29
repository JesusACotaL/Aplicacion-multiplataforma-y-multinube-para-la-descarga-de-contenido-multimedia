"""
MAIN API ENDPOINT for Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0
pip install -r requirements.txt
pip freeze > requirements.txt
"""
from importlib import import_module
import json
import io
import time
import requests
import os
import uuid
from threading import Thread
from PIL import Image

print("=== STARTING MAIN API ENDPOINT ===")
print("Loading sources from file... ",end="")
mangaEndpoints = []
mangaInfoEndpoints = []
with open('endpoints.json','r') as f:
    endpoints = json.load(f)
    mangaEndpoints = endpoints['mangaEndpoints']
    mangaInfoEndpoints = endpoints['mangaInfoEndpoints']
print("success")

print("Connecting to local manga database... ",end="")
import dbConnector
print("success")

# Create connection to firebase and keep it alive
print("Connecting to firebase... ",end="")
from IArecomendaciones import obtener_generos, obtener_recomendaciones # Start conection on AI module as well
from firebase_admin import credentials, firestore,  initialize_app, auth, storage
cred = credentials.Certificate('firebase-credentials.json')
initialize_app(cred)
db = firestore.client()
print("success")

from flask import Flask, request, jsonify, make_response, send_file, send_from_directory
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<string:path>')
@app.route('/<path:path>')
def frontend(path):
    if '.' in path: # if file requested
        if path.endswith(".js" or ".mjs"): 
            return send_from_directory('mangafront', path, mimetype="application/javascript")
        return send_from_directory('mangafront', path)
    else:
        return send_from_directory('mangafront', 'index.html') # angular router will handle the rest

@app.route("/mangaAPI/")
def info():
    return "<p>Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0</p>"

@app.route("/mangaAPI/mangaDB/<path:path>")
def mangaDBFolder(path):
    return send_from_directory('mangaDB', path)

@app.post("/mangaAPI/getTopMangasInSources")
def getTopMangasInSources():
    data = request.json
    limit = int(data['limit'])
    topmangas = []
    for endpoint in mangaInfoEndpoints:
        if(endpoint['enabled'] == True):
            print("Getting top mangas for "+endpoint['name'])
            body = {"limit": limit+50}
            url = endpoint['url'] + "/getTopMangas"
            res = requests.post(url, json=body)
            res.raise_for_status()
            result = json.loads(res.content)
            if(type(result) == list):
                results = []
                for res in result:
                    data = {}
                    data['url'] = res
                    data['srcName'] = endpoint['name']
                    results.append(data)
                topmangas = topmangas + results
            time.sleep(1)
    return topmangas[::-1]

@app.post("/mangaAPI/insertMangaDB")
def insertMangaDB():
    data = request.json
    url = data['url']
    srcName = data['srcName']
    for endpoint in mangaInfoEndpoints:
        if(endpoint['name'] == srcName and endpoint['enabled'] == True):
            print("Scrapping "+url+" ...",end="")
            time.sleep(1)
            requrl = endpoint['url'] + "/getMangaInfo"
            body = {"url": url}
            res = requests.post(requrl, json=body)
            res.raise_for_status()
            result = json.loads(res.content)
            if(type(result) is dict):
                manga = result
                print("Saving to db...")
                manga['srcName'] = srcName
                dbConnector.insertManga(manga)
    return {'status':'done', 'totalMangas':dbConnector.getLocalDBMeta()['totalMangas']}

@app.post("/mangaAPI/getMangaFromLocalDB")
def getMangaFromLocalDB():
    data = request.json
    id = data['id']
    manga = dbConnector.getManga(id)
    return manga

@app.post("/mangaAPI/searchMangaInLocalDB")
def searchMangaInLocalDB():
    data = request.json
    searchQuery = data['manga']
    safeSearch = data['safeSearch']
    mangas = dbConnector.searchManga(searchQuery, safeSearch)
    return mangas

@app.post("/mangaAPI/searchGenreInLocalDB")
def searchGenreInLocalDB():
    data = request.json
    searchQuery = data['genre']
    mangas = dbConnector.searchGenre(searchQuery)
    return mangas

@app.post("/mangaAPI/clearChapterCacheDB")
def clearChapterCacheDB():
    data = request.json
    confirmation = data['confirm']
    if(confirmation):
        def deletedb():
            print('DELETING CACHE FOR CHAPTERS!')
            dbConnector.deleteChapterCache()
            print('CHAPTER CACHE DELETED!')
        thread = Thread(target=deletedb)
        thread.start()
    return { 'result': 'Chapter cache clearing started.'}

@app.post("/mangaAPI/nukeLocalDB")
def nukeLocalDB():
    data = request.json
    confirmation = data['confirm']
    if(confirmation):
        def deletedb():
            print('DELETING DATABASE DATA AND FILES!')
            dbConnector.deleteDatabase()
            print('DATABASE DELETED!')
        thread = Thread(target=deletedb)
        thread.start()
    return { 'result': 'Database clearing started.'}


@app.get("/mangaAPI/getLocalDBmetadata")
def getLocalDBmetadata():
    res = dbConnector.getLocalDBMeta()
    return res

@app.post("/mangaAPI/searchManga")
def searchManga():
    data = request.json
    srcName = data['srcName']
    searchQuery = data['manga']
    body = {"manga": searchQuery}
    mangas = []
    for endpoint in mangaInfoEndpoints:
        if (endpoint['name'] == srcName and endpoint['enabled'] == True):
            try:
                url = endpoint['url'] + "/searchManga"
                res = requests.post(url, json=body)
                res.raise_for_status()
                result = json.loads(res.content)
                if(type(result) is list):
                    for manga in result:
                        manga['srcName'] = endpoint['name']
                    mangas = result[:25] # Only 25 results
            except:
                print("Endpoint failure: " + endpoint["name"])
    return mangas

@app.post("/mangaAPI/saveMangaInfo")
def saveMangaInfo():
    data = request.json
    srcInfoName = data['srcInfoName']
    url = data['url']
    body = {"url": url}
    manga = {}
    for endpoint in mangaInfoEndpoints:
        if (endpoint['name'] == srcInfoName and endpoint['enabled'] == True):
            url = endpoint['url'] + "/getMangaInfo"
            res = requests.post(url, json=body)
            res.raise_for_status() 
            result = json.loads(res.content)
            if(type(result) is dict):
                manga = result
                manga['srcName'] = srcInfoName
                id = dbConnector.insertManga(manga)
                manga['id'] = id
    return manga

@app.post("/mangaAPI/setMangaEndpoints")
def setMangaEndpoints():
    global mangaEndpoints, mangaInfoEndpoints
    data = request.json
    if(type(data) is list):
        print('Setting new mangaendpoints...')
        mangaEndpoints, mangaInfoEndpoints = data[0], data[1]
    return {'mangaEndpoints':mangaEndpoints,'mangaInfoEndpoints':mangaInfoEndpoints}

@app.get("/mangaAPI/getMangaEndpoints")
def getMangaEndpoints():
    endpoints = []
    for endpoint in mangaEndpoints:
        endpoints.append(endpoint)
    return endpoints

@app.get("/mangaAPI/getMangaInfoEndpoints")
def getMangaInfoEndpoints():
    endpoints = []
    for endpoint in mangaInfoEndpoints:
        endpoints.append(endpoint)
    return endpoints

@app.post("/mangaAPI/insertEndpoint")
def insertEndpoint():
    global mangaEndpoints
    data = request.json
    newEndpoint = data['endpoint']
    mangaEndpoints.append(newEndpoint)
    return {'mangaEndpoints':mangaEndpoints,'mangaInfoEndpoints':mangaInfoEndpoints}

@app.post("/mangaAPI/insertInfoEndpoint")
def insertInfoEndpoint():
    global mangaInfoEndpoints
    data = request.json
    newEndpoint = data['endpoint']
    mangaInfoEndpoints.append(newEndpoint)
    return {'mangaEndpoints':mangaEndpoints,'mangaInfoEndpoints':mangaInfoEndpoints}

@app.post("/mangaAPI/updateEndpoint")
def updateEndpoint():
    global mangaEndpoints
    global mangaInfoEndpoints
    data = request.json
    endpointData = data['endpoint']
    newEndpoints = []
    newInfoEndpoints = []
    for endpoint in mangaEndpoints:
        if(endpoint['name'] != endpointData['name']):
            newEndpoints.append(endpoint)
        else:
            newEndpoints.append(endpointData)
    for endpoint in mangaInfoEndpoints:
        if(endpoint['name'] != endpointData['name']):
            newInfoEndpoints.append(endpoint)
        else:
            newInfoEndpoints.append(endpointData)
    mangaEndpoints = newEndpoints
    mangaInfoEndpoints = newInfoEndpoints
    return {'mangaEndpoints':mangaEndpoints,'mangaInfoEndpoints':mangaInfoEndpoints}

@app.post("/mangaAPI/removeEndpoint")
def removeEndpoint():
    global mangaEndpoints
    global mangaInfoEndpoints
    data = request.json
    endpointData = data['endpoint']
    newEndpoints = []
    newInfoEndpoints = []
    for endpoint in mangaEndpoints:
        if(endpoint['name'] != endpointData['name']):
            newEndpoints.append(endpoint)
    for endpoint in mangaInfoEndpoints:
        if(endpoint['name'] != endpointData['name']):
            newInfoEndpoints.append(endpoint)
    mangaEndpoints = newEndpoints
    mangaInfoEndpoints = newInfoEndpoints
    return {'mangaEndpoints':mangaEndpoints,'mangaInfoEndpoints':mangaInfoEndpoints}

@app.post("/mangaAPI/findMangaInEndpoint")
def findMangaInEndpoint():
    data = request.json
    searchQuery = data['manga']
    sourceName = data['source']
    body = {"manga": searchQuery}
    mangas = []
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName and endpoint['enabled'] == True):
            try:
                url = endpoint['url'] + "/searchManga"
                res = requests.post(url, json=body)
                res.raise_for_status()
                result = json.loads(res.content)
                if(type(result) is list):
                    temp = result[:5] # Only 5 sources per manga
                    for i in temp:
                        i['srcName'] = endpoint['name'] # Include source name in results
                    mangas = mangas + temp
            except:
                print("Endpoint failure: " + endpoint["name"])
    return mangas

@app.post("/mangaAPI/getCachedChapters")
def getCachedChapters():
    data = request.json
    mangaID = data['mangaID']
    # Get any cached chapters first on the list
    cachedChapters = dbConnector.getCachedChapters(mangaID)
    return cachedChapters

@app.post("/mangaAPI/getMangaChapters")
def getMangaChapters():
    data = request.json
    url = data['url']
    sourceName = data['source']
    body = {"url": url}
    chapters = []
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName and endpoint['enabled'] == True):
            try:
                url = endpoint['url'] + "/getMangaChapters"
                res = requests.post(url, json=body)
                res.raise_for_status()
                result = json.loads(res.content)
                if(type(result) is list):
                    temp = result
                    for i in temp:
                        i['srcName'] = endpoint['name'] # Include source name in results
                    chapters = chapters + temp
            except:
                print("Endpoint failure: " + endpoint["name"])
    return chapters

@app.post("/mangaAPI/getChapterURLS")
def getChapterURLS():
    data = request.json
    chapterName = data['chapterName']
    mangaID = data['mangaID']
    url = data['url']
    sourceName = data['source']
    body = {"url": url}
    images = []
    test = dbConnector.checkIfChapterExists(url)
    if(test):
        for i in test:
            tempRes = {}
            tempRes['url'] = i
            tempRes['srcName'] = sourceName # Include source name in results
            images.append(tempRes)
        return images
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName and endpoint['enabled'] == True):
            try:
                url = endpoint['url'] + "/getChapterURLS"
                res = requests.post(url, json=body)
                res.raise_for_status()
                result = json.loads(res.content)
                if(type(result) is list):
                    temp = result
                    dbConnector.insertChapter(chapterName, mangaID, data['url'], sourceName, json.dumps(temp)) # Cache chapter
                    for i in temp:
                        tempRes = {}
                        tempRes['url'] = i
                        tempRes['srcName'] = sourceName # Include source name in results
                        images.append(tempRes)
            except:
                print("Endpoint failure: " + endpoint["name"])
    return images

@app.post("/mangaAPI/getChapterImage")
def getChapterImage():
    data = request.json
    chapterURL = data['chapterURL']
    sourceName = data['source']
    newurl = ''
    cached = dbConnector.checkIfCachedImage(data['url'])
    if(not cached):
        for endpoint in mangaEndpoints:
            if(endpoint["name"] == sourceName and endpoint['enabled'] == True):
                urlreq = endpoint['url'] + "/getImageBlob"
                body = {"url": data['url']}
                res = requests.post(urlreq, json=body)
                res.raise_for_status()
                result = res.content
                if(type(result) is bytes):
                    newurl = dbConnector.cacheChapterImage(chapterURL, data['url'], result)
    else:
        newurl = data['url']
    return {'url':newurl}

@app.post("/mangaAPI/getImageBlob")
def getImageBlob():
    data = request.json
    url = data['url']
    quality = int(data['quality'])
    if(quality > 100 or quality < 1 ):
        quality = 50
    sourceName = data['source']
    body = {"url": url}
    imageBlob = {}
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName and endpoint['enabled'] == True):
            try:
                url = endpoint['url'] + "/getImageBlob"
                res = requests.post(url, json=body)
                res.raise_for_status()
                result = res.content
                if(type(result) is bytes):
                    # Save image as JPEG format, and apply image compression, number must be in %
                    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg-saving
                    buffer = io.BytesIO(result)
                    imgPIL = Image.open(buffer)
                    imgPIL = imgPIL.convert('RGB')
                    buffer2 = io.BytesIO()
                    imgPIL.save(buffer2,format='JPEG',optimize=True,quality=quality)
                    buffer3 = io.BytesIO(buffer2.getvalue())
                    imageBlob = send_file(buffer3, mimetype='image/jpeg')
            except:
                print("Endpoint failure: " + endpoint["name"])
    return imageBlob

@app.post("/mangaAPI/addToTopManga")
def addToTopManga():
    data = request.json
    import datetime
    now = datetime.datetime.now()
    # Verify existance
    manga = db.collection('topmanga').where('name', '==', data['name']).get()
    if len(manga) == 0:
        # Create url for image in firestore if exists
        url = ''
        if(data['img'] != ''):
            # https://stackoverflow.com/questions/52451215/find-the-url-of-uploaded-file-firebase-storage-python#:~:text=You%20can%20get%20the%20public%20url%20with%20blob.public_url,blob%20%3D%20bucket.blob%20%28BLOB_PATH%29%20blob.upload_from_filename%20%28FILE_PATH%29%20print%20%28blob.public_url%29
            filename = data['img'][1:] # Remove first backlash
            with open(filename, mode='rb') as file:
                fileContent = file.read()
                unique_filename = str(uuid.uuid4()) + '.jpg'
                filePath = 'mangaIMG/' + unique_filename;
                bucket = storage.bucket('mango-ec7e1.appspot.com')
                blob = bucket.blob(filePath)
                blob.upload_from_string(fileContent, content_type="image/jpeg")
                blob.make_public()
                url = blob.public_url
        newtopmanga = {
            'name': data['name'],
            'img': url,
            'originURL': data['originURL'],
            'srcName': data['srcName'],
            'viewcount': 1
        }
        # Add with 1 view count
        db.collection('topmanga').add(newtopmanga)
    else:
        # Update view count
        olddata = manga[0].to_dict()
        olddata['viewcount'] = olddata['viewcount'] + 1
        db.collection('topmanga').document(manga[0].id).set(olddata)
    return {'result': str(data['id']) + ' added to topmanga correctly'}

@app.get("/mangaAPI/getTopManga")
def getTopManga():
    query = db.collection('topmanga').order_by("viewcount", direction=firestore.Query.DESCENDING).limit(10).get()
    topmanga = []
    for doc in query:
        manga = doc.to_dict()
        topmanga.append(manga)
    return topmanga

def getUserRatings(uid):
    # Fetch all user ratings
    query = db.collection('ratings').where('uid', '==', uid).get()

    # Generate list and return it
    userRatings = []
    for doc in query:
        title = doc.get('title')
        rating = float(doc.get('ratings'))
        userRatings.append({
            'name': title,
            'rating': rating
        })
    return userRatings

@app.post("/mangaAPI/user/getUserGenres")
def getUserGenres():
    data = request.json
    uid = data['uid']
    userInput = getUserRatings(uid)
    userGenres = obtener_generos(userInput)[:5] # Max 5 genres
    return userGenres

@app.post("/mangaAPI/user/getUserRecomendations")
def getUserRecomendations():
    data = request.json
    uid = data['uid']
    userInput = getUserRatings(uid)
    mangas = obtener_recomendaciones(userInput)
    return mangas

@app.post("/mangaAPI/user/getMangaRating")
def getMangaRating():
    data = request.json
    uid = data['uid']
    title = data['title']
    query = db.collection('ratings').where('uid', '==', uid)
    query = query.where('title', '==', title).get()
    userRatings = []
    for doc in query:
        rating = int(doc.get('ratings'))
        userRatings.append({
            'rating': rating
        })
    return userRatings[0] if (len(userRatings) > 0) else ''

@app.post("/mangaAPI/user/rate")
def rateManga():
    data = request.json
    # Verify existance
    ratings_collection = db.collection('ratings').where('uid', '==', data['uid'])
    query = ratings_collection.where('title', '==', data['title']).get()
    # Set rating to 0 if invalid
    rating = data['rating']
    if(rating != '1' and rating != '2' and rating != '3' and rating != '4' and rating != '5'):
        rating = 0
    if len(query) == 0:
        # Add
        new_rating = {
            'uid': data['uid'],
            'title': data['title'],
            'ratings': rating
        }
        db.collection('ratings').add(new_rating)
    else:
        # Update
        document_ref = db.collection('ratings').document(query[0].id)
        updated_rating = {
            'ratings': rating
        }
        document_ref.update(updated_rating)
    return {'result': 'Rating operation succesful'}

@app.post("/mangaAPI/user/updateEmail")
def updateUserEmail():
    data = request.json
    uid = data['uid']
    mail = data['email']
    auth.update_user(uid, email= mail)
    user_ref = db.collection("users").document(uid)
    user_ref.update({"email": mail})
    return {'result': 'E-Mail Successfully Updated'}


@app.post("/mangaAPI/user/updatePassword")
def updateUserPassword():
    data = request.json
    uid = data['uid']
    passw = data['password']
    auth.update_user(uid, password = passw)
    return {'result': 'Password Successfully Updated'}

@app.post("/mangaAPI/user/addMangaToBookmarks")
def addMangaToBookmarks():
    data = request.json
    # Verify existance
    bookmarks = db.collection('bookmarks').where('uid', '==', data['uid'])
    query = bookmarks.where('name', '==', data['name']).get()
    if len(query) == 0:
        # Create url for image in firestore if exists
        # https://stackoverflow.com/questions/52451215/find-the-url-of-uploaded-file-firebase-storage-python#:~:text=You%20can%20get%20the%20public%20url%20with%20blob.public_url,blob%20%3D%20bucket.blob%20%28BLOB_PATH%29%20blob.upload_from_filename%20%28FILE_PATH%29%20print%20%28blob.public_url%29
        url = ''
        if(data['img'] != ''):
            filename = data['img'][1:] # Remove first backlash
            with open(filename, mode='rb') as file:
                fileContent = file.read()
                unique_filename = str(uuid.uuid4()) + '.jpg'
                filePath = 'mangaIMG/' + unique_filename;
                bucket = storage.bucket('mango-ec7e1.appspot.com')
                blob = bucket.blob(filePath)
                blob.upload_from_string(fileContent, content_type="image/jpeg")
                blob.make_public()
                url = blob.public_url
        # Add
        newbookmark = {
            'uid': data['uid'],
            'name': data['name'],
            'img': url,
            'originURL': data['originURL'],
            'srcName': data['srcName']
        }
        db.collection('bookmarks').add(newbookmark)
    return {'result': str(data['id']) + ' added to bookmarks correctly'}

@app.post("/mangaAPI/user/removeMangaFromBookmarks")
def removeMangaFromBookmarks():
    data = request.json
    uid = data['uid']
    id = data['id']
    # Verify existance
    bookmarks = db.collection('bookmarks').where('uid', '==', uid)
    query = bookmarks.where('id', '==', id).get()
    if len(query) > 0:
        # Remove
        db.collection('bookmarks').document(query[0].id).delete()
    return {'result': str(data['id']) + ' removed from bookmarks correctly'}

@app.post("/mangaAPI/user/getBookmarks")
def getBookmarks():
    data = request.json
    bookmarks = db.collection('bookmarks').where('uid', '==', data['uid']).get()
    mangas = []
    for bookmark in bookmarks:
        mangas.append(bookmark.to_dict())
    return mangas

@app.post("/mangaAPI/user/addToHistory")
def addToHistory():
    data = request.json
    import datetime
    now = datetime.datetime.now()
    # Verify existance
    history = db.collection('history').where('uid', '==', data['uid'])
    query = history.where('name', '==', data['name']).get()
    if len(query) == 0:
        # Create url for image in firestore if exists
        # https://stackoverflow.com/questions/52451215/find-the-url-of-uploaded-file-firebase-storage-python#:~:text=You%20can%20get%20the%20public%20url%20with%20blob.public_url,blob%20%3D%20bucket.blob%20%28BLOB_PATH%29%20blob.upload_from_filename%20%28FILE_PATH%29%20print%20%28blob.public_url%29
        url = ''
        if(data['img'] != ''):
            filename = data['img'][1:] # Remove first backlash
            with open(filename, mode='rb') as file:
                fileContent = file.read()
                unique_filename = str(uuid.uuid4()) + '.jpg'
                filePath = 'mangaIMG/' + unique_filename;
                bucket = storage.bucket('mango-ec7e1.appspot.com')
                blob = bucket.blob(filePath)
                blob.upload_from_string(fileContent, content_type="image/jpeg")
                blob.make_public()
                url = blob.public_url
        newhistory = {
            'uid': data['uid'],
            'name': data['name'],
            'img': url,
            'originURL': data['originURL'],
            'srcName': data['srcName'],
            'datetime': now
        }
        # Add
        db.collection('history').add(newhistory)
    else:
        manga = query[0].to_dict()
        manga['datetime'] = now
        # Update view date
        db.collection('history').document(query[0].id).set(manga)
    return {'result': str(data['id']) + ' added to user history correctly'}

@app.post("/mangaAPI/user/getHistory")
def getHistory():
    data = request.json
    # Remember that firebase requires an index if you want to manage complex queries beyond a single field
    collection = db.collection('history').where('uid', '==', data['uid'])
    query = collection.order_by("datetime", direction=firestore.Query.DESCENDING).limit(20).get()
    mangas = []
    for manga in query:
        mangas.append(manga.to_dict())
    return mangas

@app.post("/mangaAPI/uploadBackground")
def uploadBackground():
    file = request.files['file']
    if(file):
        res = dbConnector.uploadFile(file)
        return { 'file': res}
    return {'file': None}

if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app)
    app.run(host='0.0.0.0', port=5000, debug=True)