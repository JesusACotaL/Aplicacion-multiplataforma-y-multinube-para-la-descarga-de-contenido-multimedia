import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from 'src/environments/environment';
import { MangaApiService } from '../services/manga-api.service';
import { Manga } from '../interfaces/manga.interface';

@Component({
  selector: 'app-genre',
  templateUrl: './genre.component.html',
  styleUrls: ['./genre.component.css']
})
export class GenreComponent implements OnInit {

  genero = ''
  mangasEncontradosDBLocal: Array<Manga> = [];
  fuentesInfo: Array<any> = []
  backend = environment.mainMangaAPI;
  cargandoLocal = true;
  
  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    // Obtener busqueda de genero
    this.route.params.subscribe( (parametros) => {
      this.genero = parametros['name'];
      this.buscarLocal(); 
    });
  }

  buscarLocal() {
    this.mangaAPI.buscarGeneroLocalDB(this.genero).subscribe( (mangasLocal) => {
      this.mangasEncontradosDBLocal = mangasLocal;
      this.cargandoLocal = false;
    });
  }

  verManga(id: number) {
    return '/manga?' + new URLSearchParams({id: id.toString()}).toString()
  }

}
