import { Injectable } from "@angular/core";
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, signInWithPopup, GoogleAuthProvider, browserSessionPersistence} from "@angular/fire/auth";
import { User, onAuthStateChanged, setPersistence } from 'firebase/auth'; // Importar User de firebase/auth
import { FirebaseApp } from '@angular/fire/app';
import { AngularFirestore } from '@angular/fire/compat/firestore';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Manga } from "../interfaces/manga.interface";
import * as bootstrap from 'bootstrap';
import { Router } from "@angular/router";

@Injectable({
    providedIn:'root'
})
export class UserService{

    backend = 'http://127.0.0.1:5000'
    currentUser = this.auth.currentUser;   

    constructor(private auth:Auth,private firestore: AngularFirestore,private http: HttpClient, private router: Router){
        setPersistence(this.auth, browserSessionPersistence);
    }

    register({email, password}: any){
        return createUserWithEmailAndPassword(this.auth, email, password)
          .then(response => {
            this.saveUserToFirestore(response.user);
            return response;
          });
    }

    openLoginWindow() {
        const loginModal: bootstrap.Modal = new bootstrap.Modal('#loginModal', {keyboard: false});
        loginModal.show();
    }

    login({email,password}: any){
        return signInWithEmailAndPassword(this.auth,email,password);
    }

    logout(){
        signOut(this.auth).then(()=>{
          this.router.navigate(['/home']).then(() => {
            window.location.reload();
          });
        }).catch(error => console.log(error));
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

    rateManga(uid: string, title: string, rating: string) {
        const body = {
          uid: uid,
          title: title,
          rating: rating
        }
        const url = `${this.backend}/user/rate`;
        return this.http.post<any>(url,body);
    }
      
    getMangaRating(uid: string, title: string) {
        const body = {
            uid: uid,
            title: title
        }
        const url = `${this.backend}/user/getMangaRating`;
        return this.http.post<any>(url,body);
    }

    updateUserEmail(uid: string, email: string){
        const body = {
            uid: uid,
            email: email
        }
        const url = `${this.backend}/user/updateEmail`;
        return this.http.post<any>(url,body);
    }

    updateUserPassword(uid: string, password: string){
        const body = {
            uid: uid,
            password: password
        }
        const url = `${this.backend}/user/updatePassword`;
        return this.http.post<any>(url,body);
    }

    getUserRecommendations(uid: string) {
        const body = {
            uid: uid
        }
        const url = `${this.backend}/user/getUserRecomendations`;
        return this.http.post<any>(url,body);
    }

    getUserGenres(uid: string) {
        const body = {
            uid: uid
        }
        const url = `${this.backend}/user/getUserGenres`;
        return this.http.post<any>(url,body);
    }

    getHistory(uid: string) {
        const body = {
            uid: uid
        }
        const url = `${this.backend}/user/getHistory`;
        return this.http.post<any>(url,body);
    }

    addToHistory(uid: string, manga: Manga) {
        const body = {
            uid: uid,
            ... manga
        }
        const url = `${this.backend}/user/addToHistory`;
        return this.http.post<any>(url,body);
    }

    getBookmarks(uid: string) {
        const body = {
            uid: uid
        }
        const url = `${this.backend}/user/getBookmarks`;
        return this.http.post<any>(url,body);
    }

    addMangaToBookmarks(uid: string, manga: Manga) {
        const body = {
            uid: uid,
            ... manga
        }
        const url = `${this.backend}/user/addMangaToBookmarks`;
        return this.http.post<any>(url,body);
    }

    removeMangaFromBookmarks(uid: string, manga: Manga) {
        const body = {
            uid: uid,
            ... manga
        }
        const url = `${this.backend}/user/removeMangaFromBookmarks`;
        return this.http.post<any>(url,body);
    }
}