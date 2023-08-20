import { Component, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-source-config-modal',
  templateUrl: './source-config-modal.component.html',
  styleUrls: ['./source-config-modal.component.css']
})
export class SourceConfigModalComponent implements OnInit {
  srcConfigModal!: bootstrap.Modal;
  mangaFuentes: Array<any> = []
  mangaInfoFuentes: Array<any> = []
  fuenteDefault = ""
  fuenteInfoDefault = ""

  constructor(private mangaApi: MangaApiService) { }

  ngOnInit(): void {
    this.srcConfigModal = new bootstrap.Modal('#srcConfigModal', {keyboard: false});
  }

  mostrar() {
    this.mangaApi.obtenerFuentes().subscribe( (fuentes) => {
      this.mangaFuentes = fuentes;
      this.mangaApi.obtenerFuentesInfo().subscribe( (fuentesInfo) => {
        this.mangaInfoFuentes = fuentesInfo;
        const defaultSrc = localStorage.getItem('defaultSrc');
        const defaultInfoSrc = localStorage.getItem('defaultInfoSrc');
        if(defaultSrc)
          this.fuenteDefault = defaultSrc;
        if(defaultInfoSrc)
          this.fuenteInfoDefault = defaultInfoSrc;
        this.srcConfigModal.show();
      });
    });
  }

  cambiarEstadoFuente(fuenteNombre: string, estado: boolean) {
    if(estado) {
      this.mangaApi.habilitarFuente(fuenteNombre).subscribe((fuentes) => {
        this.mangaFuentes = fuentes.mangaEndpoints
        this.mangaInfoFuentes = fuentes.mangaInfoEndpoints
      });
    } else {
      this.mangaApi.deshabilitarFuente(fuenteNombre).subscribe((fuentes) => {
        this.mangaFuentes = fuentes.mangaEndpoints
        this.mangaInfoFuentes = fuentes.mangaInfoEndpoints
      });
    }
  }

  fuenteDefecto(fuenteNombre: string) {
    localStorage.setItem('defaultSrc',fuenteNombre);
  }
  fuenteInfoDefecto(fuenteNombre: string) {
    localStorage.setItem('defaultInfoSrc',fuenteNombre);
  }

}
