import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { Manga } from '../interfaces/manga.interface';
import { environment } from 'src/environments/environment';
import * as bootstrap from 'bootstrap';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  mangaBuscado = ''
  manga = '';
  mangasEncontradosDBLocal: Array<Manga> = [];
  filtroAdulto = false;
  fuentesInfo: Array<any> = []
  backend = environment.mainMangaAPI;
  cargandoLocal = true;
  totalMangaToSave = 0;
  filling = false;
  
  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    this.filtroAdulto = true ? (localStorage.getItem("filtroAdulto") == 'true') : false;
    // Obtener nombre de manga
    this.route.params.subscribe( (parametros) => {
      this.manga = parametros['name'];
      this.mangaBuscado = this.manga;
      this.buscarLocal(); 
      this.obtenerFuentesInfo();
    });
  }

  cambiarFiltroAdultos(valor: boolean) {
    localStorage.setItem("filtroAdulto",String(valor));
    this.filtroAdulto = valor;
    this.buscarLocal();
  }

  obtenerFuentesInfo() {
    this.mangaAPI.obtenerFuentesInfo().subscribe( (fuentesInfo) => {
      let newfuentes = [];
      for (const fuente of fuentesInfo) {
        let newfuente: any = {};
        newfuente.nombre = fuente;
        newfuente.cargando = true;
        newfuente.mangasEncontrados = [];
        newfuentes.push(newfuente);
      }
      this.fuentesInfo = newfuentes;
    });
  }

  buscarLocal() {
    this.mangaAPI.buscarMangaLocalDB(this.manga, this.filtroAdulto).subscribe( (mangasLocal) => {
      this.mangasEncontradosDBLocal = mangasLocal;
      this.cargandoLocal = false;
    });
  }
  
  buscarFuente(fuente: string) {
    for (const f of this.fuentesInfo) {
      if(fuente == f.nombre) {
        this.mangaAPI.buscarManga(this.manga, fuente).subscribe( (resultados) => {
          f.mangasEncontrados = resultados;
          f.cargando = false;
        });
      }
    }
  }

  verManga(id: number) {
    return '/manga?' + new URLSearchParams({id: id.toString()}).toString()
  }
  verMangaLink(url: string) {
    return '/manga?' + new URLSearchParams({id: url}).toString()
  }

  async saveResultsToDB(mangas: Array<any>) {
    this.totalMangaToSave = mangas.length;
    const modal = new bootstrap.Modal('#saveToDBModal', {keyboard: false});
    modal.show();
    const logContainer = document.getElementById('saveToDBModallogContainer');
    const span = document.createElement('span');
    logContainer!.innerHTML = '';
    this.filling = true;
    span.innerText = `Found ${mangas.length} mangas.`
    logContainer?.append(span.cloneNode(true));
    const delay = (ms:any) => new Promise(res => setTimeout(res, ms));
    for (const manga of mangas) {
      if(this.filling) {
        await new Promise<void>(resolve => {
          span.innerText = `Saving ${manga.url}...`
          logContainer?.append(span.cloneNode(true));
          this.mangaAPI.subirMangaDB(manga.url, manga.srcName).subscribe((result)=>{
            this.totalMangaToSave = this.totalMangaToSave - 1;
            resolve();
          })
        });
        await delay(2000);
      }
    }
    span.innerText = 'Operation finished.'
    logContainer?.append(span.cloneNode(true));
    this.filling = false;
  }

  cancelFill() {
    this.filling = false;
  }

}
