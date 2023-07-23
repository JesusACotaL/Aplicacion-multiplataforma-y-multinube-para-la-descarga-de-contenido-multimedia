import { Component, Input, OnChanges, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';
import { MangaApiService } from '../services/manga-api.service';
import { jsPDF } from "jspdf";
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-manga-modal',
  templateUrl: './manga-modal.component.html',
  styleUrls: ['./manga-modal.component.css']
})
export class MangaModalComponent implements OnInit { 
  mangaModal!: bootstrap.Modal;
  div!: HTMLElement | null;
  titulo!: string;
  cargadas = 0;
  total = 0;
  mostrando = false;
  obteniendoLinks = true;
  calidad = "75";

  fuenteActualNombre = ""
  fuenteActualURL = ""
  
  constructor(private mangaAPI: MangaApiService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.mangaModal = new bootstrap.Modal('#exampleModal', {keyboard: false});
    this.div = document.getElementById('ImagenesCapitulo');
  }
  
  mostrar(nombreEpisodio: string, fuenteNombre: string, fuente:string) {
    if(fuente != '' && this.div) {
      this.mangaModal.show();
      this.div.innerHTML = '';
      this.fuenteActualNombre = fuenteNombre;
      this.fuenteActualURL = fuente;
      this.cargarImagenes();
    }
    this.titulo = nombreEpisodio;
    this.mostrando = true;
  }

  closeModal() {
    const queryParams: Params = { chap: null, title: null, chapSrcName: null };
    this.router.navigate(
      [], 
      {
        relativeTo: this.route,
        queryParams: queryParams, 
        queryParamsHandling: 'merge', // remove to replace all query params by provided
    });
    this.mostrando = false;
  }

  cambiarCalidad(valor: string) {
    this.calidad = valor;
    this.div!.innerHTML = '';
    this.cargarImagenes();
  }

  cargarImagenes() {
    const fuente_nombre = this.fuenteActualNombre; 
    const url = this.fuenteActualURL;
    this.obteniendoLinks = true;
    this.mangaAPI.obtenerLinksCapitulo(fuente_nombre, url).subscribe( async (imagenes: Array<any>) => {
      this.cargadas = 0;
      this.total = imagenes.length;
      this.obteniendoLinks = false;
      for (const imagen of imagenes) {
        if(this.mostrando) { // Cancel if user closed modal
          await new Promise<void>(resolve => {
            this.mangaAPI.descargarImagenCapitulo(imagen['source'], imagen['url'], parseInt(this.calidad)).subscribe( ( imagenBlob ) => {
              let htmlimg = new Image();
              htmlimg.className = "img-fluid";
              const url = window.URL.createObjectURL(imagenBlob);
              htmlimg.src = url
              htmlimg.onload = (evt) => {
                window.URL.revokeObjectURL(url);
              }
              this.div?.append(htmlimg);
              this.cargadas = this.cargadas + 1;
              resolve();
            });
          });
        }
      }
    });
  }

  loadingImages() {
    if(this.obteniendoLinks || this.total > this.cargadas) return true;
    else return false;
  }

  descargarEpisodio() {
    if(!this.loadingImages) return;
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'px',
      format: 'letter'
    });
    if(this.div) {
      let imgCollection = Array.from(this.div.children);
      for (let i = 0; i < imgCollection.length; i++) {
        const img = imgCollection[i];
        const imgWidth = img.clientWidth;
        const imgHeight = img.clientHeight;
        console.log('Image #'+i+' size: '+'w='+imgWidth+'h='+imgHeight);
        const imgRatio = imgWidth / imgHeight;
        if (imgRatio >= 1) {
            pdf.addPage([imgWidth, imgHeight], 'landscape');
        } else {
            pdf.addPage([imgWidth, imgHeight], 'portrait');
        }
        let pageHeight = pdf.internal.pageSize.getHeight();
        let pageWidth = pdf.internal.pageSize.getWidth();
        //pdf.setPage(i + 2);
        pdf.addImage(img.getAttribute('src')!, 'JPEG', 0, 0, imgWidth, imgHeight);
      }
      pdf.deletePage(1); // first page is by default blank in jspdf
      pdf.save(this.titulo+".pdf");
    }
  }

}
