import { Component, OnInit } from '@angular/core';
import { MangaApiService } from '../services/manga-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  manga = '';

  constructor(private mangaAPI: MangaApiService, private router: Router) { }

  ngOnInit(): void {
  }

  buscarManga() {
    this.router.navigate(['/buscar',this.manga]);
  }

}
