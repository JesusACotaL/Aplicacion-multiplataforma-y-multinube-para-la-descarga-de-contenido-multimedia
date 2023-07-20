export interface Manga {
    mangaID: string,
    name: string,
    name_english: string,
    authors: string,
    background: string,
    characters: Array<any>,
    date: string,
    genres: string,
    img: string,
    site: string,
    statistics: {
        popularity: string,
        ranked: string,
        score: string,
        scoreUsers: string
    },
    status: string,
    synopsis: string,
    mangaURL: string
}