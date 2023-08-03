"""
MAIN API ENDPOINT for Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0
"""
from importlib import import_module
import json
import io
import requests
from PIL import Image

mangaInfoEndpoints = [
    {
        "name": "myanimelist",
        "url": "http://myanimelistapi:5000"
    }
]
mangaEndpoints = [
    {
        "name": "manganelo",
        "url": "http://manganelo:5000"
    },
    {
        "name": "mangakakalottv",
        "url": "http://mangakakalottv:5000"
    },
    {
        "name": "mangakakalotcom",
        "url": "http://mangakakalotcom:5000"
    }
]

print("=== STARTING MAIN API ENDPOINT ===")

# Create connection to firebase and keep it alive
print("Connecting to database... ",end="")
from backendIA.recomendaciones import obtener_generos, obtener_recomendaciones # Start conection on AI module as well
from firebase_admin import credentials, firestore,  initialize_app, auth
cred = credentials.Certificate('firebase-credentials.json')
initialize_app(cred)
db = firestore.client()
print("success")

from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def info():
    return "<p>Aplicacion multiplataforma y multinube para la descarga de contenido multimedia API v1.0</p>"

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
                mangas = mangas + result
        except:
            print("Endpoint failure: " + endpoint["name"])
    return mangas

@app.post("/getMangaInfo")
def getMangaInfo():
    data = request.json
    url = data['url']
    body = {"url": url}
    manga = {}
    for endpoint in mangaInfoEndpoints:
        try:
            url = endpoint['url'] + "/getMangaInfo"
            res = requests.post(url, json=body)
            res.raise_for_status()
            result = json.loads(res.content)
            if(type(result) is dict):
                manga = result
        except:
            print("Endpoint failure: " + endpoint["name"])
    return manga

@app.post("/findMangaInEndpoints")
def findMangaInEndpoints():
    data = request.json
    searchQuery = data['manga']
    body = {"manga": searchQuery}
    mangas = []
    for endpoint in mangaEndpoints:
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
    manga = db.collection('topmanga').where('mangaID', '==', data['mangaID']).get()
    newtopmanga = {
        'mangaID': data['mangaID'],
        'name': data['name'],
        'img': data['img'],
        'mangaURL': data['mangaURL'],
        'viewcount': 1
    }
    if len(manga) == 0:
        # Add with 1 view count
        db.collection('topmanga').add(newtopmanga)
    else:
        # Update view count
        olddata = manga[0].to_dict()
        newtopmanga['viewcount'] = olddata['viewcount'] + 1
        db.collection('topmanga').document(manga[0].id).set(newtopmanga)
    return {'result': str(data['mangaID']) + ' added to topmanga correctly'}

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
    userGenres = obtener_recomendaciones(userInput)
    return userGenres

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
    query = bookmarks.where('mangaID', '==', data['mangaID']).get()
    if len(query) == 0:
        # Add
        newbookmark = {
            'uid': data['uid'],
            'mangaID': data['mangaID'],
            'name': data['name'],
            'img': data['img'],
            'mangaURL': data['mangaURL']
        }
        db.collection('bookmarks').add(newbookmark)
    return {'result': str(data['mangaID']) + ' added to bookmarks correctly'}

@app.post("/user/removeMangaFromBookmarks")
def removeMangaFromBookmarks():
    data = request.json
    uid = data['uid']
    mangaID = data['mangaID']
    # Verify existance
    bookmarks = db.collection('bookmarks').where('uid', '==', uid)
    query = bookmarks.where('mangaID', '==', mangaID).get()
    if len(query) > 0:
        # Remove
        db.collection('bookmarks').document(query[0].id).delete()
    return {'result': str(data['mangaID']) + ' removed from bookmarks correctly'}

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
    query = history.where('mangaID', '==', data['mangaID']).get()
    newhistory = {
        'uid': data['uid'],
        'mangaID': data['mangaID'],
        'name': data['name'],
        'img': data['img'],
        'mangaURL': data['mangaURL'],
        'datetime': now
    }
    if len(query) == 0:
        # Add
        db.collection('history').add(newhistory)
    else:
        # Update view date
        db.collection('history').document(query[0].id).set(newhistory)
    return {'result': str(data['mangaID']) + ' added to user history correctly'}

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