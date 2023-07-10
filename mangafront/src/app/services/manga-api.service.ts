import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class MangaApiService {

  backend = 'http://127.0.0.1:5000'
  constructor(private http: HttpClient) {}

  buscarManga(nombre: string): Observable<any>{
    const body = {
      manga: nombre
    }
    const url = `${this.backend}/searchManga`;
    return this.http.post<any>(url,body);
  }

  obtenerMangaInfo(manga_url: string): Observable<any>{
    const body = {
      url: manga_url
    }
    const url = `${this.backend}/getMangaInfo`;
    return this.http.post<any>(url,body);
  }

  encontrarFuentes(manga: string): Observable<any>{
    const body = {
      manga: manga
    }
    const url = `${this.backend}/findMangaSource`;
    return this.http.post<any>(url,body);
  }
  
  obtenerCapitulos(mangaURL: string): Observable<any>{
    const body = {
      url: mangaURL
    }
    const url = `${this.backend}/getMangaChapters`;
    return this.http.post<any>(url,body);
  }

  obtenerLinksCapitulo(capituloURL: string): Observable<any>{
    const body = {
      url: capituloURL
    }
    const url = `${this.backend}/getChapterLinks`;
    return this.http.post<any>(url,body);
  }

  descargarImagenCapitulo(imagenURL: string): Observable<any>{
    const body = {
      url: imagenURL
    }
    let options = {
      headers: new HttpHeaders({
         'Accept':'image/jpeg'
      }),
      'responseType': 'text' as 'json'
    } 
    const url = `${this.backend}/downloadChapterImage`;
    return this.http.post<any>(url,body,options);
  }

  obtenerBusquedasPopulares() {
    return this.http.get('assets/datosPrueba/get-popular-search.json');
  }
}
