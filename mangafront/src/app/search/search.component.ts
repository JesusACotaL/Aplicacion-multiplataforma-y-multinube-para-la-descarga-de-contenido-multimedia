import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  cargando = true;
  mangaBuscado = ''
  manga = '';
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
    this.mangaAPI.buscarManga(this.manga, this.filtroAdulto).subscribe( (mangas) => {
      this.mangasEncontrados = mangas;
      this.mangaBuscado = this.manga
      this.cargando= false;
    });
  }

  verMangaLink(url: string) {
    return '/manga?' + new URLSearchParams({manga: url}).toString()
  }

}
