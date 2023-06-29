import { Component, OnInit } from '@angular/core';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-pruebas-api',
  templateUrl: './pruebas-api.component.html',
  styleUrls: ['./pruebas-api.component.css']
})
export class PruebasAPIComponent implements OnInit {

  constructor(private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    // Ejecutar pruebas al iniciar
    this.buscarManga();
    this.buscarCapitulos();
    this.obtenerLinks();
    this.obtenerArchivo();
  }
  
  buscarManga() {
    const nombre = 'one piece';
    this.mangaAPI.buscarManga(nombre).subscribe( (datos) => {
      console.log('Buscando manga: '+nombre);
      console.log(datos);
    });
  }

  buscarCapitulos() {
    const mangaURL = 'https://chapmanganelo.com/manga-aa88620';
    this.mangaAPI.obtenerCapitulos(mangaURL).subscribe( (datos) => {
      console.log('Buscando capitulos de manga: '+mangaURL);
      console.log(datos);
    });
  }
  
  obtenerLinks() {
    const capituloURL = 'https://chapmanganelo.com/manga-aa88620/chapter-1'
    this.mangaAPI.obtenerLinksCapitulo(capituloURL).subscribe( (datos) => {
      console.log('Buscando imagenes de capitulo: '+capituloURL);
      console.log(datos);
    });
  }
  
  obtenerArchivo() {
    // const nombreArchivo = 'ejemplo.pdf';
    // const imagenesURLs = [
    //   'asd.jpg',
    //   'asd2.jpg'
    // ];
    // this.mangaAPI.descargarImagenCapitulo(nombreArchivo, imagenesURLs).subscribe( (datos) => {
    //   console.log('Generando archivo: '+nombreArchivo);
    //   console.log(datos);
    // });
  }
}
