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
export class MangaModalComponent implements OnInit, OnChanges {
  fuenteManga: string; 
  mangaModal!: bootstrap.Modal;
  div!: HTMLElement | null;
  titulo!: string;
  @Input() pFuenteMangaNombre: string;
  @Input() pFuenteManga: string;
  @Input() pTitulo: string;
  @Input() pMostrar: boolean;
  cargadas = 0;
  total = 0;
  
  constructor(private mangaAPI: MangaApiService, private router: Router, private route: ActivatedRoute) {
    this.pFuenteMangaNombre = '';
    this.pFuenteManga = '';
    this.pTitulo = '';
    this.pMostrar=false;
    this.fuenteManga = '';
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
    const queryParams: Params = { chap: this.fuenteManga, title: this.titulo, chapSrcName: this.pFuenteMangaNombre };
    this.router.navigate(
      [], 
      {
        relativeTo: this.route,
        queryParams: queryParams, 
        queryParamsHandling: 'merge', // remove to replace all query params by provided
    });
    this.mangaModal.show();
    if(this.div) {
      this.div.innerHTML = '';
    }
    if(this.fuenteManga != '') {
      this.cargarImagenes(this.pFuenteMangaNombre, this.fuenteManga);
    }
  }

  closeModal() {
    const queryParams: Params = { chap: null, title: null };
    this.router.navigate(
      [], 
      {
        relativeTo: this.route,
        queryParams: queryParams, 
        queryParamsHandling: 'merge', // remove to replace all query params by provided
    });
    this.titulo = '';
    this.fuenteManga = '';
  }

  cargarImagenes(fuente_nombre: string, url: string) { 
    this.mangaAPI.obtenerLinksCapitulo(fuente_nombre, url).subscribe( async (imagenes: Array<any>) => {
      this.cargadas = 0;
      this.total = imagenes.length;
      for (const imagen of imagenes) {
        if(this.fuenteManga != '') { // Cancel if user closed modal
          await new Promise<void>(resolve => {
            this.mangaAPI.descargarImagenCapitulo(imagen['source'], imagen['url']).subscribe( ( imagenBase64 ) => {
              let htmlimg = new Image();
              htmlimg.className = "img-fluid";
              htmlimg.src = 'data:image/jpeg;base64,'+imagenBase64;
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
    if(this.total > this.cargadas) return true;
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
