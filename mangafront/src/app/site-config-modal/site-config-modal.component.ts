import { Component, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';
import { MangaApiService } from '../services/manga-api.service';
import { environment } from 'src/environments/environment';
import { Router } from '@angular/router';

@Component({
  selector: 'app-site-config-modal',
  templateUrl: './site-config-modal.component.html',
  styleUrls: ['./site-config-modal.component.css']
})
export class SiteConfigModalComponent implements OnInit {
  siteConfigModal!: bootstrap.Modal;
  populatingDBModal!: bootstrap.Modal;
  dbSize = 0
  totalMangas = 0
  filesSize = 0
  mangaCacheSize = 0
  themeColor = '#441f89'
  backend = environment.mainMangaAPI
  filling = false
  mangaFetchAmount = 100

  constructor(private mangaAPI: MangaApiService, router: Router) {
  }
  
  ngOnInit(): void {
    this.siteConfigModal = new bootstrap.Modal('#siteConfigModal', {keyboard: false});
    this.populatingDBModal = new bootstrap.Modal('#populatingDBModal', {keyboard: false});
    const color = localStorage.getItem('themeColor');
    if(color) {
      this.themeColor = color;
      this.switchTheme(color);
    }
    const backgroundImg = localStorage.getItem('backgroundImg');
    if(backgroundImg)
      this.setBackgroundImg(backgroundImg);
    else
      this.setBackgroundImg('assets/fondo.jpg')
  }

  mostrar() {
    this.siteConfigModal.show()
    this.mangaAPI.obtenerDBmeta().subscribe((datos)=>{
      this.filesSize = datos['filesSize']
      this.dbSize = datos['dbSize']
      this.totalMangas = datos['totalMangas']
      this.mangaCacheSize = datos['mangaCacheSize']
    });
  }

  ocultar() {
    this.siteConfigModal.hide();
  }

  borrarDB() {
    const confirmation = confirm("WARNING!\nThis will delete ALL files and mangas in DB. This is irreversible.\nAre you sure you want to continue?");
    if(confirmation) {
      this.mangaAPI.borrarDB().subscribe((data)=>console.log(data));
      localStorage.setItem('backgroundImg','');
    }
  }
  
  borrarCapitulosDB() {
    const confirmation = confirm("This will delete ALL cached tomes. \nDo you want to continue?");
    if(confirmation) {
      this.mangaAPI.borrarCapitulosDB().subscribe((data)=>console.log(data));
      localStorage.setItem('backgroundImg','');
    }
  }

  hexToHSL(hex: string) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    let r = parseInt(result![1], 16);
    let g = parseInt(result![2], 16);
    let b = parseInt(result![3], 16);

    r /= 255, g /= 255, b /= 255;
    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h: number, s: number, l: number = (max + min) / 2;

    if (max == min){
        h = s = 0; // achromatic
    } else {
        var d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        
        h! /= 6;
    }

    h = Math.round(h!*360);
    s = Math.round(s*100);
    l = Math.round(l*100);

    return { h, s, l };
  }

  switchTheme(color: string) {
    let val = this.hexToHSL(color);
    console.log(val);
    var r = document.querySelector(':root') as HTMLElement;
    if(r) {
        r.style.setProperty('--base-color', val.h.toString()) 
        r.style.setProperty('--base-saturation', val.s.toString()+'%') 
        // r.style.setProperty('--background','#FFF');
        // r.style.setProperty('--text-color', '#000');
        localStorage.setItem('themeColor',color);
    }
  }

  setBackgroundImg(url: string) {
    var r = document.querySelector(':root') as HTMLElement;
    if(r)
      r.style.setProperty('--background','url("'+url+'")');
  }

  changeBackground(file: File | undefined) {
    if(file) {
      this.mangaAPI.subirBackground(file).subscribe((respuesta) => {
        if(respuesta.file) {
          const url = this.backend + respuesta.file
          localStorage.setItem('backgroundImg',url);
          this.setBackgroundImg(url);    
        }
      });
    }
  }

  cancelFill() {
    this.filling = false
  }

  fillDatabase() {
    const logContainer = document.getElementById('logContainer');
    const span = document.createElement('span');
    logContainer!.innerHTML = '';
    this.filling = true;
    span.innerText = `Obtaining manga list, please wait...`
    logContainer?.append(span.cloneNode(true));
    this.mangaAPI.obtenerTopMangasFuentes(this.mangaFetchAmount).subscribe(async (mangas) => {
      span.innerText = `Found ${mangas.length} mangas.`
      logContainer?.append(span.cloneNode(true));
      const delay = (ms:any) => new Promise(res => setTimeout(res, ms));
      for (const manga of mangas) {
        if(this.filling) {
          await new Promise<void>(resolve => {
            span.innerText = `Saving ${manga.url}...`
            logContainer?.append(span.cloneNode(true));
            this.mangaAPI.subirMangaDB(manga.url, manga.srcName).subscribe((result)=>{
              this.totalMangas = result.totalMangas
              resolve();
            })
          });
          await delay(2000);
        }
      }
      span.innerText = 'Operation finished.'
      logContainer?.append(span.cloneNode(true));
      this.filling = false;
    })
  }

}
