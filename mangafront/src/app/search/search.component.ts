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

  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    // Obtener nombre de manga
    this.route.params.subscribe( (parametros) => {
      this.manga = parametros['name'];
      this.buscarAPI();  
    });
  }
  
  buscarAPI() {
    this.cargando = true;
    // Buscar manga en API
    this.mangaAPI.buscarManga(this.manga).subscribe( (mangas) => {
      this.mangasEncontrados = mangas;
      this.mangaBuscado = this.manga
      this.cargando= false;
    });
  }

  verMangaLink(url: string) {
    return '/manga?' + new URLSearchParams({manga: url}).toString()
  }

}
