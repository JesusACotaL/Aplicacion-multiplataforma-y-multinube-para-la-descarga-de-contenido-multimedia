import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { Manga } from '../interfaces/manga.interface';

@Component({
  selector: 'app-buscar',
  templateUrl: './buscar.component.html',
  styleUrls: ['./buscar.component.css']
})
export class BuscarComponent implements OnInit {
  cargando = true;
  mangaBuscado = ''
  manga = '';
  mangasEncontrados: Manga[] = [
    {
      name: '',
      author: '',
      image_url: '',
      chapters_url: '',
      stars: ''
    }
  ];

  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService, private router: Router) { }

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
      console.log('Mangas encontrados:');
      console.log(mangas);
      this.mangasEncontrados = mangas;
      this.mangaBuscado = this.manga
      this.cargando= false;
    });
  }

  verManga(manga: Manga) {
    this.router.navigate(['/manga',manga.name]);
  }

}
