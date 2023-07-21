import { Component, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';

@Component({
  selector: 'app-user-license',
  templateUrl: './user-license.component.html',
  styleUrls: ['./user-license.component.css']
})
export class UserLicenseComponent implements OnInit {
  mangaModal!: bootstrap.Modal;

  constructor() { }

  ngOnInit(): void {
    this.mangaModal = new bootstrap.Modal('#licenseModal', {keyboard: false});
    this.checarLicencia();
  }
  
  mostrarLicencia() {
    this.mangaModal.show();
  }

  ocultarLicencia() {
    this.mangaModal.hide();
  }
  
  checarLicencia() {
    let status = localStorage.getItem('licencia');
    if(status != 'aceptada') {
      // Mostrar licencia para aceptar
      this.mostrarLicencia();
    }
  }

  guardarLicencia() {
    localStorage.setItem('licencia','aceptada');
  }

}
