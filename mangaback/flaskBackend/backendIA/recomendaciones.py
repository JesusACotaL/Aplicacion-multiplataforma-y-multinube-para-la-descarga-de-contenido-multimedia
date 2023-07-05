import pandas as pd
import itertools
import os

def obtener_recomendaciones(userInput):
    # Reading manga information into a pandas dataframe
    mangas_df = pd.read_csv('mangas.csv')
    mangas_df['genres'] = mangas_df.genres.str.split(', ')

    # Copying the manga dataframe into a new one since we won't need to use the genre information in our first case.
    mangasWithGenres_df = mangas_df.copy()

    # For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
    for index, row in mangas_df.iterrows():
        for genre in row['genres']:
            mangasWithGenres_df.at[index, genre] = 1
    # Filling in the NaN values with 0 to show that a manga doesn't have that column's genre
    mangasWithGenres_df = mangasWithGenres_df.fillna(0)

    #print("Mangas Codificadas:\n", mangasWithGenres_df)

    #print("Ratings: \n", ratings_df.head())

    # Drop removes a specified row or column from a dataframe
    #print('Rating Nuevo: \n', ratings_df.head())

    inputMangas = pd.DataFrame(userInput)

    #print('Mangas Usuario:\n', inputMangas)

    # Filtering out the mangas by title
    inputId = mangas_df[mangas_df['title'].isin(inputMangas['title'].tolist())]
    # Then merging it so we can get the mangaId. It's implicitly merging it by title.
    inputMangas = pd.merge(inputId, inputMangas)
    # Dropping information we won't use from the input dataframe
    inputMangas = inputMangas.drop('genres', axis=1)
    # Final input dataframe
    # If a manga you added in above isn't here, then it might not be in the original
    # dataframe or it might spelled differently, please check capitalisation.

    # Filtering out the mangas from the input
    userMangas = mangasWithGenres_df[mangasWithGenres_df['mangaId'].isin(inputMangas['mangaId'].tolist())]
    #print("Mangas Usuario Codificadas: \n", userMangas)

    # Resetting the index to avoid future issues
    userMangas = userMangas.reset_index(drop=True)
    # Dropping unnecessary issues due to save memory and to avoid issues
    userGenreTable = userMangas.drop('mangaId', axis=1).drop('title', axis=1).drop('genres', axis=1)
    #print("Tabla de generos: \n", userGenreTable)

    # Dot produt to get weights
    userProfile = userGenreTable.transpose().dot(inputMangas['rating'])
    # The user profile
    #print("Categoría que el Usuario Prefiere: \n", userProfile);

    # Now let's get the genres of every manga in our original dataframe
    genreTable = mangasWithGenres_df.set_index(mangasWithGenres_df['mangaId'])
    # And drop the unnecessary information
    genreTable = genreTable.drop('mangaId', axis=1).drop('title', axis=1).drop('genres', axis=1)
    #('Generos:\n', genreTable.head())
    genreTable.shape

    # Multiply the genres by the weights and then take the weighted average
    recommendationTable_df = ((genreTable * userProfile).sum(axis=1)) / (userProfile.sum())
    #print("Recomendaciones:\n", recommendationTable_df.head())

    # Sort our recommendations in descending order
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
    # Just a peek at the values
    #print('Recomendaciones:\n', recommendationTable_df.head())

    recomendaciones = recommendationTable_df.head()
    mangaIds = recomendaciones.index.tolist()
    titulos_recomendaciones = []
    for mangaId in mangaIds:
        manga = mangas_df.loc[mangas_df['mangaId'] == mangaId]
        titulo = manga['title'].values[0]
        generos = manga['genres'].values[0]
        titulo_con_generos = f"{titulo} - {generos}"
        titulos_recomendaciones.append({
            'titulo': titulo,
            'generos': generos,
        })

    return titulos_recomendaciones

def obtener_generos(userInput):
    mangas_df = pd.read_csv('mangas.csv')
    mangas_df['genres'] = mangas_df.genres.str.split(', ')

    mangasWithGenres_df = mangas_df.copy()

    for index, row in mangas_df.iterrows():
        for genre in row['genres']:
            mangasWithGenres_df.at[index, genre] = 1
    mangasWithGenres_df = mangasWithGenres_df.fillna(0)

    inputMangas = pd.DataFrame(userInput)

    inputId = mangas_df[mangas_df['title'].isin(inputMangas['title'].tolist())]
    inputMangas = pd.merge(inputId, inputMangas)
    inputMangas = inputMangas.drop('genres', axis=1)

    userMangas = mangasWithGenres_df[mangasWithGenres_df['mangaId'].isin(inputMangas['mangaId'].tolist())]

    userMangas = userMangas.reset_index(drop=True)
    userGenreTable = userMangas.drop('mangaId', axis=1).drop('title', axis=1).drop('genres', axis=1)

    userProfile = userGenreTable.transpose().dot(inputMangas['rating'])
    generos_seleccionados = userProfile[userProfile > 0]

    generos_lista = list(set(itertools.chain(*[genre.split(', ') for genre in generos_seleccionados.index])))

    return generos_lista