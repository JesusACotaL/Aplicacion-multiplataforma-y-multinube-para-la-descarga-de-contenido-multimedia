export interface MangaCharacter {
    name: string,
    role: string
    image: string
    url: string
}

export interface Manga {
    id: number,
    name: string,
    originURL: string,
    date: string,
    status: string,
    score: string,
    popularity_rank: string,
    site: string,
    background: string,
    img: string,
    genres: Array<string>,
    authors: Array<string>,
    characters: Array<MangaCharacter>
}