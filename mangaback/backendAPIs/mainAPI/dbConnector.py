import sqlite3
con = sqlite3.connect("mangaDB.db")
cursor = con.cursor()

def createDatabase():
    """
    "name": ""
    "mangaURL": "",
    "authors": "",
    "date": "",
    "status": "",
    "genres": "",
    "characters": [
        {
            "name": "",
            "role": "",
            "image": "",
            "url": "",
        }
    ],
    "statistics": [
        {
            "score": "",
            "scoreUsers": "",
            "ranked": "",
            "popularity": "",
        }
    ],
    "site": "",
    "synopsis": "",
    "background": "",
    "img": "",
    """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manga(
        id INTEGER PRIMARY KEY,
        name TEXT,
        genres TEXT,
        authors TEXT,
        img TEXT,
        mangaURL TEXT)
    """)

def insertManga(name, genres, authors, img, mangaURL):
    cursor.execute("""
    INSERT INTO manga (name, genres, authors, img, mangaURL) VALUES 
    (?, ?, ?, ?, ?)
    """,name, genres, authors, img, mangaURL)
    con.commit()

def getMangas():
    res = cursor.execute("""
    SELECT * FROM manga;
    """);
    return res.fetchall()

if __name__ == 'main':
    pass