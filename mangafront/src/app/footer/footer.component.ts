import { Component, OnInit } from '@angular/core';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { Router } from '@angular/router';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {
  user: User | null = null;

  constructor(private userService: UserService, private router: Router) { }

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

  login(){
    this.router.navigate(['/login'])
  }

  register(){
    this.router.navigate(['/register'])
  }

  logOut(): void{
    this.userService.logout()
    .then(()=>{
      this.user = null;
    })
    .catch(error => console.log(error));
    this.router.navigate(['/'])
  }
}
