import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from './../../environments/environment';



export interface MangaSearch{
  name: string,
  image_url: string,
  autor: string,
  stars: number,
}

export interface MangaChapter{
  name: string,
  url: string,
}

@Injectable({
  providedIn: 'root'
})

export class MangaApiService {

  constructor(private http: HttpClient) {}
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
    })
  };

  getMangas(): Observable<Array<MangaSearch>>{
    let searchMangaEndpoint = `${environment.mangaApiUrl}/get-mangas`;
    const mangas = this.http.get<Array<MangaSearch>>(searchMangaEndpoint);

    return mangas
  }

  getMangasChapters(): Observable<Array<MangaChapter>>{
    let getMangaChaptersEndpoint = `${environment.mangaApiUrl}/get-mangas-chapters`;
    const chapters = this.http.get<Array<MangaChapter>>(getMangaChaptersEndpoint, );

    return chapters
  }


  getMangasImagesUrl(): Observable<Array<string>>{
    let getMangaImagesEndpoint = `${environment.mangaApiUrl}/get-mangas-urls`;

    const images_urls = this.http.get<Array<string>>(getMangaImagesEndpoint);

    return images_urls
  }
}
