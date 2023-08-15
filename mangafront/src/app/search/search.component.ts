import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { Manga } from '../interfaces/manga.interface';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  cargando = true;
  mangaBuscado = ''
  manga = '';
  mangasEncontradosDBLocal: Array<Manga> = [];
  mangasEncontrados: any[] = [
    {
      name: '',
      img: '',
      score: '',
      short_desc: '',
      url: ''
    }
  ];
  filtroAdulto = false;
  fuentesInfo: Array<any> = []
  backend = environment.mainMangaAPI;

  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    this.filtroAdulto = true ? (localStorage.getItem("filtroAdulto") == 'true') : false;
    // Obtener nombre de manga
    this.route.params.subscribe( (parametros) => {
      this.manga = parametros['name'];
      this.buscarAPI();  
    });
  }

  cambiarFiltroAdultos(valor: boolean) {
    localStorage.setItem("filtroAdulto",String(valor));
    this.filtroAdulto = valor;
  }
  
  buscarAPI() {
    this.cargando = true;
    // Buscar manga en API
    this.mangaAPI.buscarMangaLocalDB(this.manga, this.filtroAdulto).subscribe( (mangasLocal) => {
      this.mangasEncontradosDBLocal = mangasLocal;
      this.mangaAPI.buscarManga(this.manga, this.filtroAdulto).subscribe( (fuentesEncontradas) => {
        this.fuentesInfo = fuentesEncontradas;
        this.mangaBuscado = this.manga
        this.cargando= false;
      });
    });
  }

  verManga(id: number) {
    return '/manga?' + new URLSearchParams({id: id.toString()}).toString()
  }
  verMangaLink(url: string) {
    return '/manga?' + new URLSearchParams({id: url}).toString()
  }

}
