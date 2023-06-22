import { Injectable } from "@angular/core";
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, signInWithPopup, GoogleAuthProvider, browserSessionPersistence} from "@angular/fire/auth";
import { User, onAuthStateChanged, setPersistence } from 'firebase/auth'; // Importar User de firebase/auth
import { FirebaseApp } from '@angular/fire/app';
import { AngularFirestore } from '@angular/fire/compat/firestore';



@Injectable({
    providedIn:'root'
})
export class UserService{

    currentUser = this.auth.currentUser;   

    constructor(private auth:Auth,private firestore: AngularFirestore){
        setPersistence(this.auth, browserSessionPersistence);
    }

    register({email, password}: any){
        return createUserWithEmailAndPassword(this.auth, email, password)
          .then(response => {
            this.saveUserToFirestore(response.user);
            return response;
          });
    }

    login({email,password}: any){
        return signInWithEmailAndPassword(this.auth,email,password);
    }

    logout(){
        return signOut(this.auth);
    }

    loginWithGoogle() {
        return signInWithPopup(this.auth, new GoogleAuthProvider())
          .then(response => {
            this.saveUserToFirestore(response.user);
            return response;
          });
      }
    
    userAuthState(){
        let flag: boolean = false;
        var user = this.auth.currentUser;
        if (user){
            flag = true;
            this.currentUser = user;
        }
        else{
            flag = false;
        }
        return flag;
    }

    getAuth(){
        return this.auth;
    }

    saveUserToFirestore(user: User) {
        return this.firestore.collection('users').doc(user.uid).set({
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL,
            uid: user.uid
        });
    }

}