import { Component, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { EventEmitter } from '@angular/core';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-homescreen',
  templateUrl: './homescreen.component.html',
  styleUrls: ['./homescreen.component.css']
})
export class HomescreenComponent implements OnInit {


  ngOnInit(): void {
  }

  constructor(private router: Router, private userService: UserService) { }

  get_mangas_urls(): void{
    let nombre_manga = "/mangaka/";
    nombre_manga += ((document.getElementById("buscador_manga") as HTMLInputElement).value);
    this.router.navigate([`${nombre_manga}`]);
  }

  logIn(): void{
    this.router.navigate([`${"/login/"}`]);
  }

  signUp(): void{
    this.router.navigate([`${"/register/"}`]);
  }

  signOut(): void{
    this.userService.logout()
    .then(()=>{
      this.router.navigate([`${"/homescreen/"}`]);
      console.log("jijijaja");
    })
    .catch(error => console.log(error));
  }
}
