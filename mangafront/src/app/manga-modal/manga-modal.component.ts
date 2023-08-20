import { Component, Input, OnChanges, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';
import { MangaApiService } from '../services/manga-api.service';
import { jsPDF } from "jspdf";
import { ActivatedRoute, Params, Router } from '@angular/router';
import { environment } from 'src/environments/environment';

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
  backend = environment.mainMangaAPI;

  mangaID: number = -1;
  
  constructor(private mangaAPI: MangaApiService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.mangaModal = new bootstrap.Modal('#exampleModal', {keyboard: false});
    this.div = document.getElementById('ImagenesCapitulo');
    this.obtenerParametroCalidad();
  }
  
  mostrar(mangaID:number, nombreEpisodio: string, fuenteNombre: string, fuente:string) {
    if(fuente != '' && this.div) {
      this.mangaModal.show();
      this.div.innerHTML = '';
      this.mangaID = mangaID;
      this.fuenteActualNombre = fuenteNombre;
      this.fuenteActualURL = fuente;
      this.titulo = nombreEpisodio;
      this.cargarImagenes();
    }
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

  obtenerParametroCalidad() {
    let valor = window.localStorage.getItem("calidad");
    if(!valor) {
      valor = "75";
      window.localStorage.setItem("calidad",valor);
    }
    this.calidad = valor;
  }

  cambiarCalidad(valor: string) {
    this.calidad = valor;
    window.localStorage.setItem("calidad",valor);
  }

  recargar() {
    this.div!.innerHTML = '';
    this.cargarImagenes();
  }

  cargarImagenes() {
    const fuente_nombre = this.fuenteActualNombre; 
    const url = this.fuenteActualURL;
    this.obteniendoLinks = true;
    this.mangaAPI.obtenerLinksCapitulo(this.titulo, this.mangaID, fuente_nombre, url).subscribe( async (imagenes: Array<any>) => {
      this.cargadas = 0;
      this.total = imagenes.length;
      this.obteniendoLinks = false;
      for (const imagen of imagenes) {
        if(this.mostrando) { // Cancel if user closed modal
          await new Promise<void>(resolve => {
            this.mangaAPI.obtenerImagenURL(imagen['srcName'], imagen['url'], this.fuenteActualURL).subscribe( ( respuesta ) => {
              let htmlimg = new Image();
              htmlimg.className = "img-fluid";
              htmlimg.src = this.backend + respuesta.url
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
