import { Component, OnInit } from '@angular/core';
import { Manga } from '../interfaces/manga.interface';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-manga',
  templateUrl: './manga.component.html',
  styleUrls: ['./manga.component.css']
})
export class MangaComponent implements OnInit {
  manga = {} as Manga
  capitulos = [];
  cargando = true;

  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService) {}

  ngOnInit(): void {
    // Recuperar manga de API
    this.route.params.subscribe( (parametros) => {
      const nombre = parametros['name'];
      console.log('Nombre del manga: '+nombre);
      this.mangaAPI.buscarManga(nombre).subscribe( (mangas) => {
        this.manga = mangas[0] as Manga;
        this.obtenerCapitulos();
      });
    });
  }

  obtenerCapitulos() {
    this.cargando = true;
    this.mangaAPI.buscarCapitulos(this.manga.chapters_url).subscribe( (capitulos) => {
      console.log(capitulos.body);
      this.capitulos = capitulos.body.reverse();
      this.cargando = false;
    });
  }

}
