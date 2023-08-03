import { Component, OnInit,ViewChild,ElementRef } from '@angular/core';
import * as bootstrap from 'bootstrap';

import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth

import { AngularFirestore } from '@angular/fire/compat/firestore';

interface UserDocument {
  photoURL: string;
  // Otras propiedades que puedas tener en el documento
}

@Component({
  selector: 'app-modify-user-info-modal',
  templateUrl: './modify-user-info-modal.component.html',
  styleUrls: ['./modify-user-info-modal.component.css']
})
export class ModifyUserInfoModalComponent implements OnInit {
  @ViewChild("fileInput") fileInput!: ElementRef<HTMLInputElement>;
  accountModal!: bootstrap.Modal;
  user: User | null = null;
  profilePicture= '';

  constructor(private userService: UserService,private firestore: AngularFirestore) { }


  ngOnInit(): void {
    this.accountModal = new bootstrap.Modal('#accountModal', {keyboard: false});
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

  openFileInput() {
    // Abre el cuadro de diálogo de carga de archivos al hacer clic en la imagen del usuario
    this.fileInput.nativeElement.click();
  }

  reloadPage(){
    window.location.reload();
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files![0];
    if (file) {
      // Lógica para cargar la imagen al servicio de Firebase
      this.userService.uploadPhoto(file).subscribe(
        (url) => {
          // Actualiza la URL de la imagen en profilePicture
          this.profilePicture = url;

          const docRef = this.firestore.collection('users').doc(this.user!.uid);
          const newPic = {
            photoURL: this.profilePicture
          };
          docRef.update(newPic).then(()=>{});

        },
        (error) => {
          console.error("Error al cargar la imagen:", error);
          // Lógica adicional de manejo de errores si es necesario
        }
      );
    }
  }

  mostrar() {
    this.accountModal.show()
  }

  ocultar() {
    this.accountModal.hide();
  }

}
