import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { Auth,GoogleAuthProvider } from "@angular/fire/auth";
import { FirebaseApp } from '@angular/fire/app';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
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
  user: User | null = null;

  busquedasPopulares = [] as any

  constructor(private router: Router, private userService: UserService, private auth:Auth, private mangaAPI: MangaApiService) { }

  ngOnInit(): void {
    this.userAuthState();
    this.user = this.userService.getCurrentUser();

    // Obtener busquedas mas frecuentes
    this.mangaAPI.obtenerBusquedasPopulares().subscribe((busquedas) => {
      this.busquedasPopulares = busquedas;
    });
  }

  buscar() {
    this.router.navigate(['/buscar',this.manga]);
  }

  login(){
    this.router.navigate(['/login'])
  }

  register(){
    this.router.navigate(['/register'])
  }

  logOut(): void{
    this.userService.logout()
    .then(()=>{
      this.router.navigate(['/home']);
      this.flag = this.userService.userAuthState();
      console.log("jijijaja");
    })
    .catch(error => console.log(error));
  }

  userAuthState(){
    this.flag = this.userService.userAuthState();
  }

}
