import { Component, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';
import { MangaApiService } from '../services/manga-api.service';

@Component({
  selector: 'app-site-config-modal',
  templateUrl: './site-config-modal.component.html',
  styleUrls: ['./site-config-modal.component.css']
})
export class SiteConfigModalComponent implements OnInit {
  siteConfigModal!: bootstrap.Modal;
  dbSize = 0
  totalMangas = 0
  filesSize = 0

  constructor(private mangaAPI: MangaApiService) {
  }
  
  ngOnInit(): void {
    this.siteConfigModal = new bootstrap.Modal('#siteConfigModal', {keyboard: false});
  }

  mostrar() {
    this.siteConfigModal.show()
    this.mangaAPI.obtenerDBmeta().subscribe((datos)=>{
      this.filesSize = datos['filesSize']
      this.dbSize = datos['dbSize']
      this.totalMangas = datos['totalMangas']
    });
  }

  ocultar() {
    this.siteConfigModal.hide();
  }

  borrarDB() {
    this.mangaAPI.borrarDB().subscribe((data)=>console.log(data));
  }

}
