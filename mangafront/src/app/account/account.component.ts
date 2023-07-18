import { Component, OnInit } from '@angular/core';
import {Location} from '@angular/common';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { MangaApiService } from '../services/manga-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent implements OnInit {
  user: User | null = null;
  recomendados: Array<any> = []
  historial: Array<any> = []
  favoritos: Array<any> = []

  constructor( private _location: Location, private userService: UserService, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    // Recuperar usuario
    this.userService.getAuth().onAuthStateChanged((user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        this.user = user;
        this.cargarDatos();
      } else {
        // User is signed out
      }
    });
  }

  async cargarDatos() {
    await new Promise<void>(resolve => {
      this.obtenerHistorial();
      resolve();
    });
    await new Promise<void>(resolve => {
      this.obtenerRecomendados();
      resolve();
    });
    await new Promise<void>(resolve => {
      this.obtenerFavoritos();
      resolve();
    });
  }

  verMangaLink(url: string) {
    return '/manga?' + new URLSearchParams({manga: url}).toString()
  }

  volver() {
    this._location.back();
  }

  desplazarLista(direccion: boolean) {
    const lista = document.getElementById("listaMangas");
    if(!direccion)
      lista?.scrollBy({
        left: 100,
        behavior: 'smooth'
      });
    else
      lista?.scrollBy({
        left: -100,
        behavior: 'smooth'
      });
  }

  obtenerRecomendados() {
    this.userService.getUserRecommendations(this.user!.uid).subscribe( async (recommendations: Array<any>) => {
      for (const manga of recommendations) {
        await new Promise<void>(resolve => {
          this.mangaAPI.buscarManga(manga['titulo']).subscribe( ( mangas ) => {
            this.recomendados.push(mangas[0]);
            resolve();
          });
        });
      }
    });
  }

  obtenerHistorial() {
    this.userService.getHistory(this.user!.uid).subscribe( async (history: Array<any>) => {
      for (const manga of history) {
        await new Promise<void>(resolve => {
          this.mangaAPI.buscarManga(manga['manga']).subscribe( ( mangas ) => {
            this.historial.push(mangas[0]);
            resolve();
          });
        });
      }
    });
  }
  
  obtenerFavoritos() {
    this.userService.getBookmarks(this.user!.uid).subscribe( async (bookmarks: Array<any>) => {
      for (const manga of bookmarks) {
        await new Promise<void>(resolve => {
          this.mangaAPI.buscarManga(manga['manga']).subscribe( ( mangas ) => {
            this.favoritos.push(mangas[0]);
            resolve();
          });
        });
      }
    });
  }
  
  obtenerGeneros() {
    this.userService.getUserGenres(this.user!.uid).subscribe( async (genres: Array<any>) => {
      for (const genre of genres) {
        await new Promise<void>(resolve => {
          // Implementar busqueda por genero para continuar aqui
        });
      }
    });
  }

}
