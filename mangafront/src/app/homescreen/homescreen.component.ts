import { Component, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { EventEmitter } from '@angular/core';

@Component({
  selector: 'app-homescreen',
  templateUrl: './homescreen.component.html',
  styleUrls: ['./homescreen.component.css']
})
export class HomescreenComponent implements OnInit {


  ngOnInit(): void {
  }

  constructor(private router: Router) { }

  get_mangas_urls(): void{
    let nombre_manga = "/mangaka/";
    nombre_manga += ((document.getElementById("buscador_manga") as HTMLInputElement).value);
    this.router.navigate([`${nombre_manga}`]);
  }
}
