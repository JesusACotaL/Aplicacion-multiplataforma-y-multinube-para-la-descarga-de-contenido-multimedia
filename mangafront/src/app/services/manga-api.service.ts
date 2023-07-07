import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class MangaApiService {

  constructor(private http: HttpClient) {}
  private backend = 'http://127.0.0.1:5000'//'https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/final';

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

  calificarManga(uid: string, title: string, rating: string) {
    const body = {
      uid: uid,
      title: title,
      ratings: rating
    }
    const url = `${this.backend}/user/rate`;
    return this.http.post<any>(url,body);
  }
  
}
