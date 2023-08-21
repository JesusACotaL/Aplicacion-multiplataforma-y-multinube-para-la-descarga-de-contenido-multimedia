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
  nuevaFuente: any = {
    enabled: true,
    name: '',
    url: ''
  }
  nuevaInfoFuente: any = {
    enabled: true,
    name: '',
    url: ''
  }

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

  insertarFuente(fuente: any) {
    this.mangaApi.insertarFuente(fuente).subscribe((fuentesActualizadas)=>{
      this.mangaFuentes = fuentesActualizadas.mangaEndpoints;
      this.mangaInfoFuentes = fuentesActualizadas.mangaInfoEndpoints;
    });
  }
  
  insertarFuenteInfo(fuente: any) {
    this.mangaApi.insertarFuenteInfo(fuente).subscribe((fuentesActualizadas)=>{
      this.mangaFuentes = fuentesActualizadas.mangaEndpoints;
      this.mangaInfoFuentes = fuentesActualizadas.mangaInfoEndpoints;
    });
  }

  actualizarFuente(fuente: any) {
    this.mangaApi.actualizarFuente(fuente).subscribe((fuentesActualizadas)=>{
      this.mangaFuentes = fuentesActualizadas.mangaEndpoints;
      this.mangaInfoFuentes = fuentesActualizadas.mangaInfoEndpoints;
    });
  }
  
  borrarFuente(fuente: any) {
    const confirmation = confirm("Delete "+fuente.name+"?");
    if(confirmation)
      this.mangaApi.borrarFuente(fuente).subscribe((fuentesActualizadas)=>{
        this.mangaFuentes = fuentesActualizadas.mangaEndpoints;
        this.mangaInfoFuentes = fuentesActualizadas.mangaInfoEndpoints;
      });
  }

  fuenteDefecto(fuenteNombre: string) {
    localStorage.setItem('defaultSrc',fuenteNombre);
  }
  fuenteInfoDefecto(fuenteNombre: string) {
    localStorage.setItem('defaultInfoSrc',fuenteNombre);
  }

}
