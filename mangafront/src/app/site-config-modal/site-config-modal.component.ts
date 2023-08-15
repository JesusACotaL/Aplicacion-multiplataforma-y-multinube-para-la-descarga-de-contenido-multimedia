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

  constructor(private mangaAPI: MangaApiService) {
  }
  
  ngOnInit(): void {
    this.siteConfigModal = new bootstrap.Modal('#siteConfigModal', {keyboard: false});
  }

  mostrar() {
    this.siteConfigModal.show()
    this.mangaAPI.checarTamanioDB().subscribe((tamanio)=>{
      this.dbSize = tamanio.size;
    });
  }

  ocultar() {
    this.siteConfigModal.hide();
  }

  borrarDB() {
    this.mangaAPI.borrarDB().subscribe((data)=>console.log(data));
  }

}
