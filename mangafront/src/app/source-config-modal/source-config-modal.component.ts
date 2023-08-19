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

  constructor(private mangaApi: MangaApiService) { }

  ngOnInit(): void {
    this.srcConfigModal = new bootstrap.Modal('#srcConfigModal', {keyboard: false});
  }

  mostrar() {
    this.mangaApi.obtenerFuentes().subscribe( (fuentes) => {
      this.mangaFuentes = fuentes;
      this.mangaApi.obtenerFuentesInfo().subscribe( (fuentesInfo) => {
        this.mangaInfoFuentes = fuentesInfo;
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

}
