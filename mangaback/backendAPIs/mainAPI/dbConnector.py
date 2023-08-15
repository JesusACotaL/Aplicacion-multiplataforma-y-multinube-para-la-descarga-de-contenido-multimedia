import sqlite3
import os 
import shutil
import json
import uuid
import requests
import math

# Local storage folder
folder = 'mangaDB' + os.sep

# Create connection
# SQLITE only allows a single thread (since it's only one file), so we inform it that we want to use it as an import
# (Otherwise we would need to open and close a conn every single time)
con = sqlite3.connect("mangas.db", check_same_thread=False)
cursor = con.cursor()

def recreateDatabase():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manga(
            id INTEGER PRIMARY KEY,
            name TEXT,
            originURL TEXT,
            date TEXT,
            status TEXT,
            score TEXT,
            popularity_rank TEXT,
            site TEXT,
            background TEXT,
            img TEXT,
            genres TEXT,
            authors TEXT,
            characters TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY,
            uuid TEXT,
            mangaID TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks(
            id INTEGER PRIMARY KEY,
            uuid TEXT,
            mangaID TEXT
        )
    """)

# Create tables if they dont exist
recreateDatabase()

def deleteDatabase():
    # Delete database
    cursor.execute("DROP TABLE IF EXISTS manga")
    cursor.execute("DROP TABLE IF EXISTS history")
    cursor.execute("DROP TABLE IF EXISTS bookmarks")
    # Recreate tables
    recreateDatabase()
    # Clear storage folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def formatAsManga(data):
    """
    "name": ""
    "originURL": "",
    "date": "",
    "status": "",
    "score": "",
    "popularity_rank": "",
    "site": "",
    "background": "",
    "img": "",
    "genres": [],
    "authors": [],
    "characters": [
        {
            "name": "",
            "role": "",
            "image": "",
            "url": "",
        }
    ]
    """
    manga = {}
    manga['id'] = data[0],
    manga['id'] = manga['id'][0] # Stupid sqlite threats id as tuple only when saving value, why?
    manga['name'] = data[1]
    manga['originURL'] = data[2]
    manga['date'] = data[3]
    manga['status'] = data[4]
    manga['score'] = data[5]
    manga['popularity_rank'] = data[6]
    manga['site'] = data[7]
    manga['background'] = data[8]
    manga['img'] = data[9]
    manga['genres'] = json.loads(data[10])
    manga['authors'] = json.loads(data[11])
    manga['characters'] = json.loads(data[12])
    return manga

def convertImagesToLocal(manga):
    # Manga Portrait
    res = requests.get(manga['img'])
    res.raise_for_status()
    imageBytes = res.content
    unique_filename = str(uuid.uuid4()) + '.jpg'
    with open(folder + unique_filename, 'wb') as f:
        f.write(imageBytes)
    manga['img']= '/mangaDB/' + unique_filename
    # Characters images
    characters = manga['characters']
    newcharacters = []
    for character in characters:
        res = requests.get(character['image'])
        res.raise_for_status()
        imageBytes = res.content
        unique_filename = uuid.uuid4().hex + '.jpg'
        with open(folder + unique_filename, 'wb') as f:
            f.write(imageBytes)
        character['image'] = '/mangaDB/' + unique_filename
        newcharacters.append(character)
    manga['characters']=newcharacters
    return manga

def insertManga(manga):
    """
    Inserts a Manga only if manga doesnt exist,
    if not, then it returns the searched manga's id
    """
    id = 0
    res = cursor.execute("""
    SELECT * FROM manga WHERE name = ?
    """,[manga['name']])
    data = res.fetchone()
    if(not data):
        manga = convertImagesToLocal(manga)
        cursor.execute("""
            INSERT INTO manga (
                name,
                originURL,
                date,
                status,
                score,
                popularity_rank,
                site,
                background,
                img,
                genres,
                authors,
                characters
            ) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                manga['name'],
                manga['originURL'],
                manga['date'],
                manga['status'],
                manga['score'],
                manga['popularity_rank'],
                manga['site'],
                manga['background'],
                manga['img'],
                json.dumps(manga['genres']),
                json.dumps(manga['authors']),
                json.dumps(manga['characters'])
            ]
        )
        con.commit()
        id = cursor.lastrowid
    else:
        id = data[0]
    return id

def getManga(id):
    res = cursor.execute("""
    SELECT * FROM manga WHERE id = ?
    """,[id])
    data = res.fetchone()
    return formatAsManga(data)

def getMangas():
    res = cursor.execute("""
    SELECT * FROM manga
    """)
    data = res.fetchall()
    mangas = []
    for manga in data:
        mangas.append(formatAsManga(manga))
    return mangas

def searchManga(manga, safeSearch=False):
    res = cursor.execute("""
    SELECT * FROM manga WHERE name LIKE ?
    """, [ '%'+manga+'%' ])
    data = res.fetchall()
    mangas = []
    for manga in data:
        manga = formatAsManga(manga)
        if(safeSearch):
            if("Hentai" not in manga['genres']):
                mangas.append(manga)
        else:
            mangas.append(manga)
    return mangas

def getUserBookmarks(uuid):
    res = cursor.execute("""
    SELECT * FROM bookmarks WHERE uuid = ?
    """,[uuid])
    data = res.fetchone()

def addMangaToBookmarks(uuid, mangaID):
    res = cursor.execute("""
    SELECT * FROM bookmarks WHERE uuid = ? AND mangaID = ?
    """,[uuid, mangaID])
    data = res.fetchone()
    if(not data):
        cursor.execute("INSERT INTO bookmarks (uuid, mangaID) VALUES (?, ?)",[uuid, mangaID])
        con.commit()

def removeMangaFromBookmarks(uuid, mangaID):
    res = cursor.execute("""
    SELECT * FROM bookmarks WHERE uuid = ? AND mangaID = ?
    """,[uuid, mangaID])
    data = res.fetchone()
    if(data):
        cursor.execute("DELETE * FROM bookmarks WHERE uuid = ? AND mangaID = ?",[uuid, mangaID])
        con.commit()

def getUserHistory(uuid):
    res = cursor.execute("""
    SELECT * FROM history WHERE uuid = ?
    """,[uuid])
    data = res.fetchone()

def addMangaToHistory():
    res = cursor.execute("""
    SELECT * FROM history WHERE uuid = ? AND mangaID = ?
    """,[uuid, mangaID])
    data = res.fetchone()
    if(not data):
        cursor.execute("INSERT INTO history (uuid, mangaID) VALUES (?, ?)",[uuid, mangaID])
        con.commit()

def removeMangaFromHistory(uuid, mangaID):
    res = cursor.execute("""
    SELECT * FROM history WHERE uuid = ? AND mangaID = ?
    """,[uuid, mangaID])
    data = res.fetchone()
    if(data):
        cursor.execute("DELETE * FROM history WHERE uuid = ? AND mangaID = ?",[uuid, mangaID])
        con.commit()

def getLocalDBMeta():
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
    filesSize = get_tree_size(folder)
    filesSize = convert_size(filesSize)
    dbSize = os.path.getsize('mangas.db')
    dbSize = convert_size(dbSize)
    totalMangas = cursor.execute("SELECT COUNT() FROM manga").fetchone()
    return {'filesSize':filesSize,'dbSize':dbSize,'totalMangas':totalMangas}

if __name__ == '__main__':
    mangas = getMangas()
    for manga in mangas:
        print(manga)