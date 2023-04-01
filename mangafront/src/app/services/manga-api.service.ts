import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class MangaApiService {

  constructor(private http: HttpClient) {}

  private manganelo = 'https://m.manganelo.com';
  private backend = 'https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/final';
  private datosPrueba = true;

  buscarManga(nombre: string): Observable<any>{
    if (this.datosPrueba) return this.http.get('assets/datosPrueba/get-manga-info.json');
    
    nombre = nombre.replace(/\ /gi,"_"); // Reemplazar espacios por _
    const body = {
      url:`${this.manganelo}/search/story/${nombre}`
    }
    const url = `${this.backend}/get-manga-info`;
    return this.http.post<any>(url,body);
  }
  
  buscarCapitulos(mangaURL: string): Observable<any>{
    if (this.datosPrueba) return this.http.get('assets/datosPrueba/get-manga-chapters.json');
    
    const body = {
      url: mangaURL
    }
    const url = `${this.backend}/get-manga-chapters`;
    return this.http.post<any>(url,body);
  }

  obtenerLinks(capituloURL: string): Observable<any>{
    if (this.datosPrueba) return this.http.get('assets/datosPrueba/get-manga-urls.json');
    
    const body = {
      url: capituloURL
    }
    const url = `${this.backend}/get-manga-urls`;
    return this.http.post<any>(url,body);
  }

  obtenerArchivo(nombreArchivo: string,imagenesURLs: string[]): Observable<any>{
    if (this.datosPrueba) return this.http.get('assets/datosPrueba/get-manga-file.json');
    
    const body = {
      format: "pdf",
      book_name: nombreArchivo,
      images_urls: imagenesURLs
    }
    const url = `${this.backend}/get-manga-file`;
    return this.http.post<any>(url,body);
  }
  
}
