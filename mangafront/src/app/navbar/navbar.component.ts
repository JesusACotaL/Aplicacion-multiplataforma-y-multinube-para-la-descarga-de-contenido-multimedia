import { Component, OnInit, ViewChild } from '@angular/core';
import { MangaApiService } from '../services/manga-api.service';
import { Router, ActivatedRoute } from '@angular/router';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { ModifyUserInfoModalComponent } from '../modify-user-info-modal/modify-user-info-modal.component';
import { AngularFirestore } from '@angular/fire/compat/firestore';

interface UserDocument {
  photoURL: string;
  // Otras propiedades que puedas tener en el documento
}

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  manga = '';
  user: User | null = null;
  @ViewChild('userInfoModal', { static: false }) userInfoModal!: ModifyUserInfoModalComponent;
  profilePicture= '';

  constructor(private mangaAPI: MangaApiService, private router: Router, private route: ActivatedRoute, private userService: UserService,private firestore: AngularFirestore) { }

  ngOnInit(): void {
    // Recuperar usuario
    this.userService.getAuth().onAuthStateChanged((user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        this.user = user;

        this.firestore.collection('users').doc(this.user.uid).get()
            .subscribe((doc) => {
              if (doc.exists) {
                const userData = doc.data() as UserDocument;
                this.profilePicture = userData.photoURL;
              } else {
                console.log("El documento no existe.");
              }
            });
            
      } else {
        // User is signed out
      }
    });
  }

  buscarManga() {
    this.router.navigate(['/search',this.manga]);
  }

  login(){
    this.userService.openLoginWindow();
  }
  
  logOut(){
    this.userService.logout();
  }

  openSignupModal() {
    this.userService.openSignUpWindow();
  }
  
  verPerfil() {
    this.router.navigate(['/home'])
  }
}
