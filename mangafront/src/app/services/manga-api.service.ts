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

  buscarManga(nombre: string, srcName: string): Observable<Array<any>>{
    const body = {
      manga: nombre,
      srcName: srcName
    }
    const url = `${this.backend}/searchManga`;
    return this.http.post<any>(url,body);
  }

  buscarMangaLocalDB(nombre: string, filtroAdulto: boolean): Observable<Array<Manga>>{
    const body = {
      manga: nombre,
      safeSearch: filtroAdulto
    }
    const url = `${this.backend}/searchMangaInLocalDB`;
    return this.http.post<any>(url,body);
  }

  obtenerMangaInfoLocalDB(id: number): Observable<Manga>{
    const body = {
      id: id
    }
    const url = `${this.backend}/getMangaFromLocalDB`;
    return this.http.post<any>(url,body);
  }

  guardarMangaInfo(manga_url: string): Observable<any>{
    const body = {
      url: manga_url
    }
    const url = `${this.backend}/saveMangaInfo`;
    return this.http.post<any>(url,body);
  }

  obtenerFuentes(): Observable<Array<string>>{
    const url = `${this.backend}/getMangaEndpoints`;
    return this.http.get<any>(url);
  }

  obtenerFuentesInfo(): Observable<Array<string>>{
    const url = `${this.backend}/getMangaInfoEndpoints`;
    return this.http.get<any>(url);
  }

  buscarEnFuente(fuenteNombre: string, manga: string): Observable<any>{
    const body = {
      source: fuenteNombre,
      manga: manga
    }
    const url = `${this.backend}/findMangaInEndpoint`;
    return this.http.post<any>(url,body);
  }
  
  obtenerCapitulos(fuenteNombre: string, originURL: string): Observable<any>{
    const body = {
      source: fuenteNombre,
      url: originURL
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

  obtenerImagenURL(fuenteNombre: string, imagenURL: string, chapterURL: string): Observable<any>{
    const body = {
      source: fuenteNombre,
      url: imagenURL,
      chapterURL: chapterURL
    }
    const url = `${this.backend}/getChapterImage`;
    return this.http.post<any>(url,body);
  }

  obtenerBusquedasPopulares(): Observable<any> {
    const url = `${this.backend}/getTopManga`;
    return this.http.get(url);
  }

  agregarBusquedaPopular(manga: Manga): Observable<any> {
    const body = {
      ... manga
    }
    const url = `${this.backend}/addToTopManga`;
    return this.http.post<any>(url,body);
  }

  obtenerDBmeta(): Observable<any> {
    const url = `${this.backend}/getLocalDBmetadata`;
    return this.http.get<any>(url);
  }

  borrarDB(): Observable<any> {
    const body = {
      confirm: true
    }
    const url = `${this.backend}/nukeLocalDB`;
    return this.http.post<any>(url,body);
  }
  
  borrarCapitulosDB(): Observable<any> {
    const body = {
      confirm: true
    }
    const url = `${this.backend}/clearChapterCacheDB`;
    return this.http.post<any>(url,body);
  }

  subirBackground(file: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    const url = `${this.backend}/uploadBackground`;
    return this.http.post<any>(url,formData);
  }

  obtenerTopMangasFuentes(cantidad: number): Observable<any> { 
    const body = {
      limit: cantidad
    }
    const url = `${this.backend}/getTopMangasInSources`;
    return this.http.post<any>(url,body);
  }
  
  subirMangaDB(mangaURL: string, srcName: string): Observable<any> { 
    const body = {
      url: mangaURL,
      srcName: srcName
    }
    const url = `${this.backend}/insertMangaDB`;
    return this.http.post<any>(url,body);
  }
}
