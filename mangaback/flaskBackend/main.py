from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from myanimelistScrapper import scrapManga, searchMangaOnline
from firebase_admin import credentials, firestore, initialize_app, auth
from backendIA.recomendaciones import obtener_generos, obtener_recomendaciones

from importlib import import_module
import json

# Create connection to firebase and keep it alive
cred = credentials.Certificate('firebase-credentials.json')
initialize_app(cred)
db = firestore.client()

# Initialize API
app = Flask(__name__)
CORS(app)

def getUserRatings(uid):
    # Fetch all user ratings
    query = db.collection('ratings').where('uid', '==', uid).get()

    # Generate list and return it
    userRatings = []
    for doc in query:
        title = doc.get('title')
        rating = float(doc.get('ratings'))
        userRatings.append({
            'title': title,
            'rating': rating
        })
    return userRatings

def readSourcesFile():
    sources = []
    with open('mangaSources.json', 'r', encoding='utf-8') as f:
        sources = json.load(f)['mangaSources']
        sources = [s for s in sources if s['enabled'] == True]
    f.close()
    return sources

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/searchManga")
def searchMangaAnimelist():
    data = request.json
    query = data['manga']
    mangas = searchMangaOnline(query)
    return jsonify(mangas)

@app.post("/getMangaInfo")
def getMangaInfoAnimelist():
    data = request.json
    url = data['url']
    mangaInfo = scrapManga(url)
    return jsonify(mangaInfo)

@app.post("/getMangaSources")
def getMangaSources():
    sources = readSourcesFile()
    return jsonify(sources)

@app.post("/addMangaSource")
def addMangaSource():
    data = request.json
    name = data['name']
    file = data['file']
    sources = readSourcesFile()
    sources.append({"name":name,"file":file})
    with open('mangaSources.json', 'w', encoding='utf-8') as f:
        sources = json.dump({"mangaSources": sources}, f)
    f.close()
    return jsonify({'result': 'Source added succesfully'})

@app.post("/removeMangaSource")
def removeMangaSource():
    data = request.json
    name = data['name']
    sources = readSourcesFile()
    sources = [s for s in sources if s['name'] != name]
    with open('mangaSources.json', 'w', encoding='utf-8') as f:
        sources = json.dump({"mangaSources": sources}, f)
    f.close()
    return jsonify({'result': 'Source removed succesfully'})

@app.post("/findMangaSource")
def findMangaSource():
    data = request.json
    manga = data['manga']
    sources = readSourcesFile()
    results = []
    for source in sources:
        sourceFile = source['file']
        moduleName = 'sources.'+sourceFile[:-3] # Remove .py extension
        module = import_module(moduleName)
        result = module.searchManga(manga)
        for res in result:
            res['source'] = source['name']
        results = results + result
    return results

@app.post("/getMangaChapters")
def getMangaChapters():
    data = request.json
    url = data['url']
    sourceName = data['source']
    sources = readSourcesFile()
    results = []
    for source in sources:
        if(source['name'] == sourceName):
            sourceFile = source['file']
            moduleName = 'sources.'+sourceFile[:-3] # Remove .py extension
            module = import_module(moduleName)
            result = module.getMangaChapters(url)
            for res in result:
                res['source'] = source['name']
            results = result
    return results

@app.post("/getChapterLinks")
def getChapterLinks():
    data = request.json
    url = data['url']
    sourceName = data['source']
    sources = readSourcesFile()
    results = []
    for source in sources:
        if(source['name'] == sourceName):
            sourceFile = source['file']
            moduleName = 'sources.'+sourceFile[:-3] # Remove .py extension
            module = import_module(moduleName)
            result = module.getChapterURLS(url)
            for res in result:
                results.append({'source':source['name'],'url':res})
    return results

@app.post("/downloadChapterImage")
def downloadChapterImage():
    data = request.json
    url = data['url']
    sourceName = data['source']
    sources = readSourcesFile()
    image_string = ''
    for source in sources:
        if(source['name'] == sourceName):
            sourceFile = source['file']
            moduleName = 'sources.'+sourceFile[:-3] # Remove .py extension
            module = import_module(moduleName)
            image_string = module.getImageBase64(url)
    response = make_response(image_string)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.post("/user/getUserGenres")
def getUserGenres():
    data = request.json
    uid = data['uid']
    userInput = getUserRatings(uid)
    userGenres = obtener_generos(userInput)
    return jsonify(userGenres)

@app.post("/user/getUserRecomendations")
def getUserRecomendations():
    data = request.json
    uid = data['uid']
    userInput = getUserRatings(uid)
    userGenres = obtener_recomendaciones(userInput)
    return jsonify(userGenres)

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
    return jsonify({'result': 'Rating operation succesful'})

@app.post("/user/updateEmail")
def updateUserEmail():
    data = request.json
    uid = data['uid']
    mail = data['email']
    auth.update_user(uid, email= mail)
    user_ref = db.collection("users").document(uid)
    user_ref.update({"email": mail})
    return jsonify({'result': 'E-Mail Successfully Updated'})


@app.post("/user/updatePassword")
def updateUserPassword():
    data = request.json
    uid = data['uid']
    passw = data['password']
    auth.update_user(uid, password = passw)
    return jsonify({'result': 'Password Successfully Updated'})

@app.post("/user/addMangaToBookmarks")
def addMangaToBookmarks():
    data = request.json
    uid = data['uid']
    manga = data['manga']
    # Verify existance
    bookmarks = db.collection('bookmarks').where('uid', '==', uid)
    query = bookmarks.where('manga', '==', manga).get()
    if len(query) == 0:
        # Add
        newbookmark = {
            'uid': uid,
            'manga': manga
        }
        db.collection('bookmarks').add(newbookmark)
    return jsonify({'result': manga + 'added to bookmarks correctly'})

@app.post("/user/removeMangaFromBookmarks")
def removeMangaFromBookmarks():
    data = request.json
    uid = data['uid']
    manga = data['manga']
    # Verify existance
    bookmarks = db.collection('bookmarks').where('uid', '==', uid)
    query = bookmarks.where('manga', '==', manga).get()
    if len(query) > 0:
        # Remove
        db.collection('bookmarks').document(query[0].id).delete()
    return jsonify({'result': manga + 'removed from bookmarks correctly'})

@app.post("/user/getBookmarks")
def getBookmarks():
    data = request.json
    uid = data['uid']
    bookmarks = db.collection('bookmarks').where('uid', '==', uid).get()
    mangas = []
    for bookmark in bookmarks:
        manga = str(bookmark.get('manga'))
        mangas.append(manga)
    return jsonify(mangas)

@app.post("/user/addToHistory")
def addToHistory():
    data = request.json
    uid = data['uid']
    manga = data['manga']
    import datetime
    now = datetime.datetime.now()
    # Verify existance
    history = db.collection('history').where('uid', '==', uid)
    query = history.where('manga', '==', manga).get()
    newhistory = {
        'uid': uid,
        'manga': manga,
        'datetime': now
    }
    if len(query) == 0:
        # Add
        db.collection('history').add(newhistory)
    else:
        # Update view date
        db.collection('bookmarks').document(query[0].id).set(newhistory)
    return jsonify({'result': manga + 'added to user history correctly'})

@app.post("/user/getHistory")
def getHistory():
    data = request.json
    uid = data['uid']
    history = db.collection('history')
    query = history.where('uid', '==', uid).get()
    mangas = []
    for item in query:
        mangas.append({
            'manga': str(item.get('manga')),
            'datetime': str(item.get('datetime'))
        })
    # Order by view date
    import time
    from dateutil.parser import parser
    p = parser()
    mangas.sort(key=lambda x:p.parse(x['datetime']))
    mangas.reverse()
    return jsonify(mangas)