import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Manga } from '../interfaces/manga.interface';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})

export class MangaApiService {

  backend = environment.mainMangaAPI;
  constructor(private http: HttpClient) {}

  buscarManga(nombre: string, filtroAdulto: boolean): Observable<any>{
    const body = {
      manga: nombre,
      safeSearch: filtroAdulto
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
    const url = `${this.backend}/findMangaInEndpoints`;
    return this.http.post<any>(url,body);
  }
  
  obtenerCapitulos(fuenteNombre: string, mangaURL: string): Observable<any>{
    const body = {
      source: fuenteNombre,
      url: mangaURL
    }
    const url = `${this.backend}/getMangaChapters`;
    return this.http.post<any>(url,body);
  }

  obtenerLinksCapitulo(fuenteNombre: string, capituloURL: string): Observable<any>{
    const body = {
      source: fuenteNombre,
      url: capituloURL
    }
    const url = `${this.backend}/getChapterURLS`;
    return this.http.post<any>(url,body);
  }

  descargarImagenCapitulo(fuenteNombre: string, imagenURL: string, calidad: number): Observable<any>{
    const body = {
      source: fuenteNombre,
      url: imagenURL,
      quality: calidad
    }
    let options = {
      headers: new HttpHeaders({
         'Accept':'image/jpeg'
      }),
      responseType: 'blob' as 'json'
    }
    const url = `${this.backend}/getImageBlob`;
    return this.http.post<any>(url,body,options);
  }

  obtenerBusquedasPopulares() {
    const url = `${this.backend}/getTopManga`;
    return this.http.get(url);
  }

  agregarBusquedaPopular(manga: Manga) {
    const body = {
      ... manga
    }
    const url = `${this.backend}/addToTopManga`;
    return this.http.post<any>(url,body);
  }
}
