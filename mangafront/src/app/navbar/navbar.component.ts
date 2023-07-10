import { Component, OnInit } from '@angular/core';
import { MangaApiService } from '../services/manga-api.service';
import { Router } from '@angular/router';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  manga = '';
  user: User | null = null;

  constructor(private mangaAPI: MangaApiService, private router: Router, private userService: UserService) { }

  ngOnInit(): void {
    // Recuperar usuario
    this.userService.getAuth().onAuthStateChanged((user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        this.user = user;
      } else {
        // User is signed out
      }
    });
  }

  buscarManga() {
    this.router.navigate(['/buscar',this.manga]);
  }

  login(){
    this.router.navigate(['/login'])
  }
  
  verPerfil() {
    this.router.navigate(['/user'])
  }
}
