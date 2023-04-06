import { Injectable } from "@angular/core";
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, signInWithPopup, GoogleAuthProvider } from "@angular/fire/auth";
import { Router } from '@angular/router';

@Injectable({
    providedIn:'root'
})
export class UserService{


    constructor(private auth:Auth,private router: Router){}

    currentUser = this.auth.currentUser;

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

    getCurrentUser(){
        return this.auth.currentUser;
    }

}