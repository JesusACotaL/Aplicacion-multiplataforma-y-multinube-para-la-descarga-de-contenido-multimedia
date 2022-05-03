import { Component, OnInit } from '@angular/core';
export interface Capitulo{
  Nombre: string
}
@Component({
  selector: 'app-mangaka',
  templateUrl: './mangaka.component.html',
  styleUrls: ['./mangaka.component.css']
})

export class MangakaComponent implements OnInit {
  capitulos: Capitulo[]=[{Nombre:"cap 1"},{Nombre:"cap 2"},{Nombre:"cap 3"}]
  constructor() { }
  ngOnInit(): void { 
  }
}



