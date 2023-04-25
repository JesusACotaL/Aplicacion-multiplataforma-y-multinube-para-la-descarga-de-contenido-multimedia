import { Component, OnInit } from '@angular/core';
import { Manga } from '../interfaces/manga.interface';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { DescargarMangaService } from '../services/descargar-manga.service';

@Component({
  selector: 'app-manga',
  templateUrl: './manga.component.html',
  styleUrls: ['./manga.component.css']
})
export class MangaComponent implements OnInit {
  manga = {} as Manga
  capitulos = [];
  cargando = true;
  capitulosPorPagina = 10;
  paginaActual = 1;
  paginas = [] as number[];
  coleccionPaginas = 1;

  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService, private descargarAPI: DescargarMangaService) {}

  ngOnInit(): void {
    // Recuperar manga de API
    this.route.params.subscribe( (parametros) => {
      const nombre = parametros['name'];
      this.mangaAPI.buscarManga(nombre).subscribe( (mangas) => {
        this.manga = mangas[0] as Manga;
        this.obtenerCapitulos();
      });
    });
  }

  obtenerCapitulos() {
    this.cargando = true;
    this.mangaAPI.buscarCapitulos(this.manga.chapters_url).subscribe( (capitulos) => {
      this.capitulos = capitulos.body.reverse();
      this.cargando = false;
      const cantPaginas = this.capitulos.length / this.capitulosPorPagina;
      for (let i = 0; i < cantPaginas; i++) {
        this.paginas.push(i+1);
      }
    });
  }

  descargarEpisodio(episodioURL: string) {
    let imagenes = this.descargarAPI.cargarImagenes('/assets/datosPrueba/img-goku-by-Jeet-Dhanoa.jpg');
    this.descargarAPI.generarPDF(imagenes);
  }

  verPagina(pagina: number) {
    this.paginaActual = pagina;
  }

  verColeccionPaginas(pagina: number) {
    this.coleccionPaginas = pagina;
    this.verPagina(pagina);
  }

}
