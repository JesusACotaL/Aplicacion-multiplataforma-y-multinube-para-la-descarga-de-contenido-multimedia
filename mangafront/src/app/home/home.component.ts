import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { Auth,GoogleAuthProvider } from "@angular/fire/auth";


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  // Como funcionan los template-driven forms: https://angular.io/guide/forms#summary
  manga = '';
  flag: boolean = false;
  

  constructor(private router: Router, private userService: UserService,private auth:Auth) { }

  ngOnInit(): void {
    this.userAuthState();
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
