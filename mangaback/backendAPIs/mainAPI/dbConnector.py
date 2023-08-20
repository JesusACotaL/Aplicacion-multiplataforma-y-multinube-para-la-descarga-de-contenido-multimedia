import sqlite3
import os 
import shutil
import json
import uuid
import requests
import math

# Local storage folder
folder = 'mangaDB'
chaptersFolder = 'chapterCache'

# Create connection
# SQLITE only allows a single thread (since it's only one file), so we inform it that we want to use it as an import
# (Otherwise we would need to open and close a conn every single time)
con = sqlite3.connect("mangas.db", check_same_thread=False)
cursor = con.cursor()

def recreateDatabase():
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder+os.sep+chaptersFolder):
        os.makedirs(folder+os.sep+chaptersFolder)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manga(
            id INTEGER PRIMARY KEY,
            name TEXT,
            originURL TEXT,
            srcName TEXT,
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
        CREATE TABLE IF NOT EXISTS chapter(
            id INTEGER PRIMARY KEY,
            chapterName TEXT,
            mangaID INTEGER,
            chapterURL TEXT,
            srcName TEXT,
            images TEXT
        )
    """)

# Create tables if they dont exist
recreateDatabase()

def deleteDatabase():
    # Delete database
    cursor.execute("DROP TABLE IF EXISTS manga")
    cursor.execute("DROP TABLE IF EXISTS chapter")
    # Recreate tables
    recreateDatabase()
    # Clear storage folder
    for filename in os.listdir(folder):
        if(filename != '.gitignore'):
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
    manga['srcName'] = data[3]
    manga['date'] = data[4]
    manga['status'] = data[5]
    manga['score'] = data[6]
    manga['popularity_rank'] = data[6]
    manga['site'] = data[8]
    manga['background'] = data[9]
    manga['img'] = data[10]
    manga['genres'] = json.loads(data[11])
    manga['authors'] = json.loads(data[12])
    manga['characters'] = json.loads(data[13])
    return manga

def cacheImage(imageURL):
    res = requests.get(imageURL)
    res.raise_for_status()
    imageBytes = res.content
    unique_filename = uuid.uuid4().hex + '.jpg'
    with open(folder + os.sep + unique_filename, 'wb') as f:
        f.write(imageBytes)
    return '/' + folder + '/' + unique_filename

def convertImagesToLocal(manga):
    # Manga Portrait
    if(manga['img'] != ''):
        res = requests.get(manga['img'])
        res.raise_for_status()
        imageBytes = res.content
        unique_filename = str(uuid.uuid4()) + '.jpg'
        with open(folder + os.sep + unique_filename, 'wb') as f:
            f.write(imageBytes)
        manga['img']= '/mangaDB/' + unique_filename
    # Characters images
    characters = manga['characters']
    newcharacters = []
    for character in characters:
        url = character['image']
        if(url != ''):
            character['image'] = cacheImage(url)
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
                srcName,
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
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                manga['name'],
                manga['originURL'],
                manga['srcName'],
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

def searchGenre(genre):
    res = cursor.execute("""
    SELECT * FROM manga WHERE genres LIKE ?
    """, [ '%'+genre+'%' ])
    data = res.fetchall()
    mangas = []
    for manga in data:
        manga = formatAsManga(manga)
        mangas.append(manga)
    return mangas

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
    mangaCacheSize = get_tree_size(folder + os.sep + chaptersFolder)
    filesSize = get_tree_size(folder)
    filesSize = convert_size(filesSize-mangaCacheSize)
    mangaCacheSize = convert_size(mangaCacheSize)
    dbSize = os.path.getsize('mangas.db')
    dbSize = convert_size(dbSize)
    totalMangas = cursor.execute("SELECT COUNT() FROM manga").fetchone()
    return {'filesSize':filesSize,'dbSize':dbSize,'totalMangas':totalMangas, 'mangaCacheSize': mangaCacheSize}

def uploadFile(file):
    ext = '.'+file.filename.rsplit('.', 1)[1].lower()
    unique_filename = uuid.uuid4().hex + ext
    file.save(folder + os.sep + unique_filename)
    return '/'+folder+'/'+unique_filename

def checkIfChapterExists(chapterURL):
    res = cursor.execute("""
    SELECT (images) FROM chapter WHERE chapterURL = ?
    """,[chapterURL])
    data = res.fetchone()
    if(data):
        images = json.loads(data[0])
        return images
    return False

def insertChapter(chapterName, mangaID, chapterURL, srcName, images):
    res = cursor.execute("""
    SELECT * FROM chapter WHERE chapterURL = ?
    """,[chapterURL])
    data = res.fetchone()
    if(not data):
        cursor.execute("INSERT INTO chapter (chapterName, mangaID, chapterURL, srcName, images) VALUES (?, ?, ?, ?, ?)",[chapterName, mangaID, chapterURL, srcName, images])
        con.commit()

def getCachedChapters(mangaID):
    res = cursor.execute("""
    SELECT chapterName, srcName, chapterURL FROM chapter WHERE mangaID = ?
    """,[mangaID])
    data = res.fetchall()
    chapters = []
    if(data):
        for chap in data:
            c = {}
            c['name'] = chap[0]
            c['srcName'] = chap[1]
            c['url'] = chap[2]
            chapters.append(c)
    return chapters

def checkIfCachedImage(imageURL):
    """
    Check if current image is already cached
    """
    if(folder in imageURL):
        return True
    return False

def cacheChapterImage(chapterURL, imageURL, imageBytes):
    # Get list of chapter images
    res = cursor.execute("""
    SELECT (images) FROM chapter WHERE chapterURL = ?
    """,[chapterURL])
    data = res.fetchone()
    images = json.loads(data[0])
    # Find image link and update it with a local link
    url = ''
    newimages = []
    for image in images:
        if(image == imageURL):
            unique_filename = uuid.uuid4().hex + '.jpg'
            with open(folder + os.sep + chaptersFolder + os.sep + unique_filename, 'wb') as f:
                f.write(imageBytes)
            url = '/' + folder + '/' + chaptersFolder + '/' + unique_filename
            image = url # Update in list
        newimages.append(image)
    # Update image list
    cursor.execute("""
    UPDATE chapter
    SET images = ?
    WHERE chapterURL = ?
    """, [json.dumps(newimages), chapterURL])
    con.commit()
    return url

def deleteChapterCache():
    # Delete database
    cursor.execute("DROP TABLE IF EXISTS chapter")
    # Recreate chapter table
    recreateDatabase()
    # Clear chapter cache folder
    newfolder = folder + os.sep + chaptersFolder
    for filename in os.listdir(newfolder):
        if(filename != '.gitignore'):
            file_path = os.path.join(newfolder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == '__main__':
    mangas = getMangas()
    for manga in mangas:
        print(manga)