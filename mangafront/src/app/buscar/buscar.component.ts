import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-buscar',
  templateUrl: './buscar.component.html',
  styleUrls: ['./buscar.component.css']
})
export class BuscarComponent implements OnInit {
  manga = '';
  mangasEncontrados = [
    {
      name: '',
      author: '',
      image_url: '',
      chapters_url: '',
      stars: ''
    }
  ];

  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    // Obtener nombre de manga
    this.route.params.subscribe( (parametros) => {
      console.log(parametros);
      this.manga = parametros['name'];
      // Buscar manga en API
      this.mangaAPI.buscarManga(this.manga).subscribe( (mangas) => {
        console.log('Mangas encontrados:');
        console.log(mangas);
        this.mangasEncontrados = mangas;
      });
    });
  }

}
