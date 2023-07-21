import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  // Como funcionan los template-driven forms: https://angular.io/guide/forms#summary
  manga = '';
  flag: boolean = false;
  busquedasPopulares = [] as any

  constructor(private router: Router, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    // Obtener busquedas mas frecuentes
    this.mangaAPI.obtenerBusquedasPopulares().subscribe((busquedas) => {
      this.busquedasPopulares = busquedas;
    });
  }

  buscar() {
    this.router.navigate(['/search',this.manga]);
  }

  verMangaLink(url: string) {
    return '/manga?' + new URLSearchParams({manga: url}).toString()
  }
}
