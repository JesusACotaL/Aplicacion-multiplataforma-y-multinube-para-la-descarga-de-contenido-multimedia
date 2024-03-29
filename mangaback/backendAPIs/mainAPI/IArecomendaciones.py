import pandas as pd
import itertools
import os
import json
import sqlite3

def getMangasInDB():
    con = sqlite3.connect("mangas.db")
    cursor = con.cursor()
    res = cursor.execute("SELECT id,name,genres,authors,img,originURL FROM manga")
    data = res.fetchall()
    mangas = []
    for item in data:
        manga = {}
        manga['id'] = item[0],
        manga['id'] = manga['id'][0] # Stupid sqlite threats id as tuple only when saving value, why?
        manga['name'] = item[1]
        manga['genres'] = json.loads(item[2])
        manga['authors'] = json.loads(item[3])
        manga['img'] = item[4]
        manga['originURL'] = item[5]
        mangas.append(manga)
    return mangas

def obtener_recomendaciones(userInput, amount=20, debug=False):
    # Reading manga information into a pandas dataframe
    # mangas_df = pd.read_csv('mangas.csv')
    # mangas_df['genres'] = mangas_df.genres.str.split(', ')
    # mangas_df.info(verbose=True)
    # print(mangas_df)
    mangas = getMangasInDB()
    mangas_df = pd.DataFrame.from_dict(mangas)
    #mangas_df.info(verbose=True)

    # Copying the manga dataframe into a new one since we won't need to use the genre information in our first case.
    mangasWithGenres_df = mangas_df.copy()

    # For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
    for index, row in mangas_df.iterrows():
        for genre in row['genres']:
            mangasWithGenres_df.at[index, genre] = 1
    # Filling in the NaN values with 0 to show that a manga doesn't have that column's genre
    mangasWithGenres_df = mangasWithGenres_df.fillna(0)
    if debug: print("New genre table: \n", mangasWithGenres_df.columns)

    inputMangas = pd.DataFrame(userInput)
    # Filtering out the mangas by name
    inputId = mangas_df[mangas_df['name'].isin(inputMangas['name'].tolist())]
    # Then merging it so we can get the id. It's implicitly merging it by name.
    inputMangas = pd.merge(inputId, inputMangas)
    # Final input dataframe
    # Dropping information we won't use from the input dataframe
    inputMangas = inputMangas.drop('genres', axis=1).drop('authors', axis=1).drop('img', axis=1).drop('originURL', axis=1)

    # Filtering out the mangas from the input
    userMangas = mangasWithGenres_df[mangasWithGenres_df['name'].isin(inputMangas['name'].tolist())]
    # Resetting the index to avoid future issues
    userMangas = userMangas.reset_index(drop=True)
    if debug: print("userMangas: \n", userMangas)

    # Dropping unnecessary issues due to save memory and to avoid issues
    userGenreTable = userMangas.drop('id', axis=1).drop('name', axis=1).drop('genres', axis=1).drop('authors', axis=1).drop('img', axis=1).drop('originURL', axis=1)
    if debug: print("Tabla de generos: \n", userGenreTable)

    # Dot produt to get weights
    userProfile = userGenreTable.transpose().dot(inputMangas['rating'])
    if debug: print("Categorías que el Usuario Prefiere: \n", userProfile);

    # Now let's get the genres of every manga in our original dataframe
    genreTable = mangasWithGenres_df.set_index(mangasWithGenres_df['id'])
    # And drop the unnecessary information
    genreTable = genreTable.drop('id', axis=1).drop('name', axis=1).drop('genres', axis=1).drop('authors', axis=1).drop('img', axis=1).drop('originURL', axis=1)
    
    # Multiply the genres by the weights and then take the weighted average
    recommendationTable_df = ((genreTable * userProfile).sum(axis=1)) / (userProfile.sum())
    # Sort our recommendations in descending order
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
    
    recomendaciones = recommendationTable_df.head(amount)
    mangaIds = recomendaciones.index.tolist()
    titulos_recomendaciones = []
    for id in mangaIds:
        manga = mangas_df.loc[mangas_df['id'] == id]
        titulos_recomendaciones.append({
            'id': int(manga['id'].values[0]),
            'name': manga['name'].values[0],
            'genres': manga['genres'].values[0],
            'authors': manga['authors'].values[0],
            'img': manga['img'].values[0],
            'originURL': manga['originURL'].values[0]
        })
    return titulos_recomendaciones

def obtener_generos(userInput):
    # mangas_df = pd.read_csv('mangas.csv')
    # mangas_df['genres'] = mangas_df.genres.str.split(', ')
    mangas = getMangasInDB()
    mangas_df = pd.DataFrame.from_dict(mangas)

    mangasWithGenres_df = mangas_df.copy()

    for index, row in mangas_df.iterrows():
        for genre in row['genres']:
            mangasWithGenres_df.at[index, genre] = 1
    mangasWithGenres_df = mangasWithGenres_df.fillna(0)

    inputMangas = pd.DataFrame(userInput)

    inputId = mangas_df[mangas_df['name'].isin(inputMangas['name'].tolist())]
    inputMangas = pd.merge(inputId, inputMangas)
    inputMangas = inputMangas.drop('genres', axis=1).drop('authors', axis=1).drop('img', axis=1).drop('originURL', axis=1)

    userMangas = mangasWithGenres_df[mangasWithGenres_df['name'].isin(inputMangas['name'].tolist())]

    userMangas = userMangas.reset_index(drop=True)
    userGenreTable = userMangas.drop('id', axis=1).drop('name', axis=1).drop('genres', axis=1).drop('authors', axis=1).drop('img', axis=1).drop('originURL', axis=1)

    userProfile = userGenreTable.transpose().dot(inputMangas['rating'])
    generos_seleccionados = userProfile[userProfile > 0]

    generos_lista = list(set(itertools.chain(*[genre.split(', ') for genre in generos_seleccionados.index])))

    return generos_lista

if __name__ == '__main__':
    userInput = [
            {'name': 'Akira', 'rating': 5},
            {'name': 'Dorohedoro', 'rating': 5},
            {'name': 'Solo Leveling', 'rating': 5},
            {'name': 'Pandora Hearts', 'rating': 1}
        ]
    # print(userInput)
    reco = obtener_recomendaciones(userInput, debug=True)
    print(reco)
    generos = obtener_generos(userInput)
    print(generos)