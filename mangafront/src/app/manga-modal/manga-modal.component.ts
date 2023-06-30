import { Component, Input, OnChanges, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-manga-modal',
  templateUrl: './manga-modal.component.html',
  styleUrls: ['./manga-modal.component.css']
})
export class MangaModalComponent implements OnInit, OnChanges {
  fuenteManga: string; 
  mangaModal!: bootstrap.Modal;
  div!: HTMLElement | null;
  titulo!: string;
  @Input() pFuenteManga: string;
  @Input() pTitulo: string;
  @Input() pMostrar: boolean;
  cargadas = 0;
  total = 0;
  
  constructor(private mangaAPI: MangaApiService) {
    this.fuenteManga = '';
    this.pFuenteManga = '';
    this.pTitulo = '';
    this.pMostrar=false;
  }

  ngOnChanges() {
    this.fuenteManga = this.pFuenteManga;   
    this.titulo = this.pTitulo
    if(this.pMostrar) {
      this.mostrar();
    }
  } 

  ngOnInit(): void {
    this.mangaModal = new bootstrap.Modal('#exampleModal', {keyboard: false});
    this.div = document.getElementById('ImagenesCapitulo');
  }
  
  mostrar() {
    this.mangaModal.show();
    if(this.div) {
      this.div.innerHTML = '';
    }
    if(this.fuenteManga != '') {
      this.cargarImagenes(this.fuenteManga);
    }
  }

  cargarImagenes(url: string) { 
    this.mangaAPI.obtenerLinksCapitulo(url).subscribe( async (imagenes: Array<string>) => {
      this.cargadas = 0;
      this.total = imagenes.length;
      for (const imagen of imagenes) {
        await new Promise<void>(resolve => {
          this.mangaAPI.descargarImagenCapitulo(imagen).subscribe( ( imagenBase64 ) => {
            let htmlimg = new Image();
            htmlimg.className = "img-fluid";
            htmlimg.src = 'data:image/jpeg;base64,'+imagenBase64;
            this.div?.append(htmlimg);
            this.cargadas = this.cargadas + 1;
            resolve();
          });
        });
      }
    });
  }

}