"""
MAIN API ENDPOINT for Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0
"""
from importlib import import_module
import json
import io
import time
import requests
import os
import math
import uuid
from PIL import Image

production = False
mangaInfoEndpoints = []
mangaEndpoints = []
if(production):
    mangaInfoEndpoints = [
        {
            "name": "myanimelist",
            "url": "https://myanimelist-qemeq7eoxq-uc.a.run.app"
        }
    ]
    mangaEndpoints = [
        {
            "name": "manganelo",
            "url": "https://manganelo-qemeq7eoxq-uc.a.run.app"
        },
        {
            "name": "mangakakalottv",
            "url": "https://mangakakalottv-qemeq7eoxq-uc.a.run.app"
        },
        {
            "name": "mangakakalotcom",
            "url": "https://mangakakalotcom-qemeq7eoxq-uc.a.run.app"
        }
    ]
else:
    mangaInfoEndpoints = [
        {
            "name": "myanimelist",
            "url": "http://127.0.0.1:5001"
        }
    ]
    mangaEndpoints = [
        {
            "name": "manganelo",
            "url": "http://127.0.0.1:5002"
        },
        {
            "name": "mangakakalottv",
            "url": "http://127.0.0.1:5003"
        },
        {
            "name": "mangakakalotcom",
            "url": "http://127.0.0.1:5004"
        }
    ]


print("=== STARTING MAIN API ENDPOINT ===")

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

from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
app = Flask(__name__, static_folder='mangaDB', static_url_path='/mangaDB')
CORS(app)

@app.route("/")
def info():
    return "<p>Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0</p>"

@app.post("/populateLocalDB")
def populateLocalDB():
    data = request.json
    limit = int(data['limit'])
    for endpoint in mangaInfoEndpoints:
        print("Getting top mangas for "+endpoint['name'])
        body = {"limit": limit}
        url = endpoint['url'] + "/getTopMangas"
        res = requests.post(url, json=body)
        res.raise_for_status()
        topMangas = json.loads(res.content)
        for url in topMangas:
            print("Scrapping "+url+" ...",end="")
            requrl = endpoint['url'] + "/getMangaInfo"
            body = {"url": url}
            res = requests.post(requrl, json=body)
            res.raise_for_status()
            result = json.loads(res.content)
            if(type(result) is dict):
                manga = result
                print("Saving to db...")
                dbConnector.insertManga(manga)
            time.sleep(1)
    return {'done'}

@app.post("/getMangaFromLocalDB")
def getMangaFromLocalDB():
    data = request.json
    id = data['id']
    manga = dbConnector.getManga(id)
    return manga

@app.post("/searchMangaInLocalDB")
def searchMangaInLocalDB():
    data = request.json
    searchQuery = data['manga']
    safeSearch = data['safeSearch']
    body = {"manga": searchQuery, "safeSearch":safeSearch}
    mangas = dbConnector.searchManga(searchQuery, safeSearch)
    return mangas

@app.post("/nukeLocalDB")
def nukeLocalDB():
    data = request.json
    confirmation = data['confirm']
    if(confirmation):
        dbConnector.deleteDatabase()
    return { 'result': 'Database cleared entirely.'}

@app.get("/getLocalDBSize")
def getLocalDBSize():
    """ Return total size of files in manga folder """
    def get_tree_size(path):
        """Return total size of files in given path and subdirs."""
        total = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                total += get_tree_size(entry.path)
            else:
                total += entry.stat(follow_symlinks=False).st_size
        return total
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
    fileSize = get_tree_size('mangaDB')
    dbSize = os.path.getsize('mangas.db')
    total = convert_size(dbSize+fileSize)
    return {'size':total}

@app.post("/searchManga")
def searchManga():
    data = request.json
    searchQuery = data['manga']
    safeSearch = data['safeSearch']
    body = {"manga": searchQuery, "safeSearch":safeSearch}
    mangas = []
    for endpoint in mangaInfoEndpoints:
        try:
            url = endpoint['url'] + "/searchManga"
            res = requests.post(url, json=body)
            res.raise_for_status()
            result = json.loads(res.content)
            if(type(result) is list):
                sourceRes = {}
                sourceRes['srcName'] = endpoint['name']
                sourceRes['mangas'] = result[:25] # Only 25 results
                mangas.append(sourceRes)
        except:
            print("Endpoint failure: " + endpoint["name"])
    return mangas

@app.post("/saveMangaInfo")
def saveMangaInfo():
    data = request.json
    url = data['url']
    body = {"url": url}
    manga = {}
    for endpoint in mangaInfoEndpoints:
        if endpoint['name'] == 'myanimelist':
            url = endpoint['url'] + "/getMangaInfo"
            res = requests.post(url, json=body)
            res.raise_for_status() 
            result = json.loads(res.content)
            if(type(result) is dict):
                manga = result
                id = dbConnector.insertManga(manga)
                manga['id'] = id
    return manga

@app.get("/getMangaEndpoints")
def getMangaEndpoints():
    endpoints = []
    for endpoint in mangaEndpoints:
        endpoints.append(endpoint['name'])
    return endpoints

@app.post("/findMangaInEndpoint")
def findMangaInEndpoint():
    data = request.json
    searchQuery = data['manga']
    sourceName = data['source']
    body = {"manga": searchQuery}
    mangas = []
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName):
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

@app.post("/getMangaChapters")
def getMangaChapters():
    data = request.json
    url = data['url']
    sourceName = data['source']
    body = {"url": url}
    chapters = []
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName):
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

@app.post("/getChapterURLS")
def getChapterURLS():
    data = request.json
    url = data['url']
    sourceName = data['source']
    body = {"url": url}
    images = []
    for endpoint in mangaEndpoints:
        if(endpoint["name"] == sourceName):
            try:
                url = endpoint['url'] + "/getChapterURLS"
                res = requests.post(url, json=body)
                res.raise_for_status()
                result = json.loads(res.content)
                if(type(result) is list):
                    temp = result
                    for i in temp:
                        tempRes = {}
                        tempRes['url'] = i
                        tempRes['srcName'] = sourceName # Include source name in results
                        images.append(tempRes)
            except:
                print("Endpoint failure: " + endpoint["name"])
    return images

@app.post("/getImageBlob")
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
        if(endpoint["name"] == sourceName):
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

@app.post("/addToTopManga")
def addToTopManga():
    data = request.json
    import datetime
    now = datetime.datetime.now()
    # Verify existance
    manga = db.collection('topmanga').where('name', '==', data['name']).get()
    if len(manga) == 0:
        # Create url for image in firestore
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

@app.get("/getTopManga")
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

@app.post("/user/getUserGenres")
def getUserGenres():
    data = request.json
    uid = data['uid']
    userInput = getUserRatings(uid)
    userGenres = obtener_generos(userInput)
    return userGenres

@app.post("/user/getUserRecomendations")
def getUserRecomendations():
    data = request.json
    uid = data['uid']
    userInput = getUserRatings(uid)
    mangas = obtener_recomendaciones(userInput)
    return mangas

@app.post("/user/getMangaRating")
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

@app.post("/user/rate")
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

@app.post("/user/updateEmail")
def updateUserEmail():
    data = request.json
    uid = data['uid']
    mail = data['email']
    auth.update_user(uid, email= mail)
    user_ref = db.collection("users").document(uid)
    user_ref.update({"email": mail})
    return {'result': 'E-Mail Successfully Updated'}


@app.post("/user/updatePassword")
def updateUserPassword():
    data = request.json
    uid = data['uid']
    passw = data['password']
    auth.update_user(uid, password = passw)
    return {'result': 'Password Successfully Updated'}

@app.post("/user/addMangaToBookmarks")
def addMangaToBookmarks():
    data = request.json
    # Verify existance
    bookmarks = db.collection('bookmarks').where('uid', '==', data['uid'])
    query = bookmarks.where('name', '==', data['name']).get()
    if len(query) == 0:
        # Create url for image in firestore
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
        # Add
        newbookmark = {
            'uid': data['uid'],
            'name': data['name'],
            'img': url,
            'originURL': data['originURL']
        }
        db.collection('bookmarks').add(newbookmark)
    return {'result': str(data['id']) + ' added to bookmarks correctly'}

@app.post("/user/removeMangaFromBookmarks")
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

@app.post("/user/getBookmarks")
def getBookmarks():
    data = request.json
    bookmarks = db.collection('bookmarks').where('uid', '==', data['uid']).get()
    mangas = []
    for bookmark in bookmarks:
        mangas.append(bookmark.to_dict())
    return mangas

@app.post("/user/addToHistory")
def addToHistory():
    data = request.json
    import datetime
    now = datetime.datetime.now()
    # Verify existance
    history = db.collection('history').where('uid', '==', data['uid'])
    query = history.where('name', '==', data['name']).get()
    if len(query) == 0:
        # Create url for image in firestore
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
        newhistory = {
            'uid': data['uid'],
            'name': data['name'],
            'img': url,
            'originURL': data['originURL'],
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

@app.post("/user/getHistory")
def getHistory():
    data = request.json
    # Remember that firebase requires an index if you want to manage complex queries beyond a single field
    collection = db.collection('history').where('uid', '==', data['uid'])
    query = collection.order_by("datetime", direction=firestore.Query.DESCENDING).limit(20).get()
    mangas = []
    for manga in query:
        mangas.append(manga.to_dict())
    return mangas

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)