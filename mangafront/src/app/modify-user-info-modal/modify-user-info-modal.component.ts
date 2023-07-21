import { Component, OnInit } from '@angular/core';
import * as bootstrap from 'bootstrap';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth

@Component({
  selector: 'app-modify-user-info-modal',
  templateUrl: './modify-user-info-modal.component.html',
  styleUrls: ['./modify-user-info-modal.component.css']
})
export class ModifyUserInfoModalComponent implements OnInit {
  accountModal!: bootstrap.Modal;
  user: User | null = null;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.accountModal = new bootstrap.Modal('#accountModal', {keyboard: false});
    // Recuperar usuario
    this.userService.getAuth().onAuthStateChanged((user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        this.user = user;        
      } else {
        // User is signed out
      }
    });
  }

  mostrar() {
    this.accountModal.show()
  }

  ocultar() {
    this.accountModal.hide();
  }

}
