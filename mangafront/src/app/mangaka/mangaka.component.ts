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
  capitulos: Capitulo[]=[{Nombre:"juan jose"},{Nombre:"diego paco"}]
  constructor() { }
  ngOnInit(): void { 
  }
}



