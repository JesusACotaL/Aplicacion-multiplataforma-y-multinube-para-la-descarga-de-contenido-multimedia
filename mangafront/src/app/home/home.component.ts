import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth

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
  user: User | null = null;
  cargando = true;

  constructor(private router: Router, private mangaAPI: MangaApiService, private userService: UserService) { }

  ngOnInit(): void {
    // Recuperar usuario
    this.userService.getAuth().onAuthStateChanged((user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        this.user = user;
      } else {
        // User is signed out
        // Obtener busquedas mas frecuentes
        this.mangaAPI.obtenerBusquedasPopulares().subscribe((busquedas) => {
          this.busquedasPopulares = busquedas;
        });
      }
      this.cargando = false;
    });
  }

  buscar() {
    this.router.navigate(['/search',this.manga]);
  }

  verMangaLink(url: string, srcInfoName: string) {
    return '/manga?' + new URLSearchParams({id: url, srcInfoName: srcInfoName}).toString()
  }
}
