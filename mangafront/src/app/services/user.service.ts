import { Injectable } from "@angular/core";
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, signInWithPopup, GoogleAuthProvider, browserSessionPersistence} from "@angular/fire/auth";
import { User, onAuthStateChanged, setPersistence } from 'firebase/auth'; // Importar User de firebase/auth
import { FirebaseApp } from '@angular/fire/app';

@Injectable({
    providedIn:'root'
})
export class UserService{

    currentUser = this.auth.currentUser;   

    constructor(private auth:Auth){
        setPersistence(this.auth, browserSessionPersistence);
    }

    register({email,password}: any){
        return createUserWithEmailAndPassword(this.auth,email,password);
    }

    login({email,password}: any){
        return signInWithEmailAndPassword(this.auth,email,password);
    }

    logout(){
        return signOut(this.auth);
    }

    loginWithGoogle(){
        return signInWithPopup(this.auth,new GoogleAuthProvider());
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

}