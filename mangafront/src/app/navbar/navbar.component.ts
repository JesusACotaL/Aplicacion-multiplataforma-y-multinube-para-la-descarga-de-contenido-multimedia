import { Component, OnInit } from '@angular/core';
import { MangaApiService } from '../services/manga-api.service';
import { Router, ActivatedRoute } from '@angular/router';

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

  constructor(private mangaAPI: MangaApiService, private router: Router, private route: ActivatedRoute, private userService: UserService) { }

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
    this.router.navigate(['/search',this.manga]);
  }

  login(){
    this.router.navigate(['/login'])
  }
  
  logOut(): void{
    this.userService.logout()
    .then(()=>{
      this.user = null;
    })
    .catch(error => console.log(error));
    this.router.navigate(['/'])
  }
  
  verPerfil() {
    this.router.navigate(['/account'])
  }
}
