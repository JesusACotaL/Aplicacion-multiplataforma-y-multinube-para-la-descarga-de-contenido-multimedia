from flask import Flask, request, jsonify, make_response
import requests
from flask_cors import CORS

from myanimelistScrapper import scrapManga, searchMangaOnline
import re
import base64

from firebase_admin import credentials, firestore, initialize_app, auth
from backendIA.recomendaciones import obtener_generos, obtener_recomendaciones

scrapperManganeloAPI = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/si"

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

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user/getUser")
def getUser():
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

@app.post("/findMangaSource")
def findMangaSource():
    data = request.json
    manga = data['manga']
    # Manganelo source
    manga = re.sub(r'\ ','_',manga) # replace whitespaces with underscores
    manga = ''.join(e for e in manga if e.isalnum() or e == '/' or e == '_' or e == ':') # remove weird characters
    manga = manga.lower() # uncapitalize
    body = {"url": "https://m.manganelo.com/search/story/"+manga}
    res = requests.post(scrapperManganeloAPI+"/get-manga-info", json=body)
    res.raise_for_status()
    return res.content

@app.post("/getMangaChapters")
def getMangaChapters():
    data = request.json
    url = data['url']
    # Manganelo source
    body = {"url": url}
    res = requests.post(scrapperManganeloAPI+"/get-manga-chapters", json=body)
    res.raise_for_status()
    return res.content

@app.post("/getChapterLinks")
def getChapterLinks():
    data = request.json
    url = data['url']
    # Manganelo source
    body = {"url": url}
    res = requests.post(scrapperManganeloAPI+"/get-manga-urls", json=body)
    res.raise_for_status()
    return res.content

@app.post("/downloadChapterImage")
def downloadChapterImage():
    data = request.json
    url = data['url']
    res = requests.get(url, headers={'referer': 'https://chapmanganelo.com/'})
    res.raise_for_status()
    image_string = base64.b64encode(res.content)
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
    return "E-Mail Successfully Updated"


@app.post("/user/updatePassword")
def updateUserPassword():
    data = request.json
    uid = data['uid']
    passw = data['password']
    auth.update_user(uid, password = passw)
    return "Password Successfully Updated"