import { Component, OnInit } from '@angular/core';
import { Manga } from '../interfaces/manga.interface';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { AngularFirestore } from '@angular/fire/compat/firestore';
import firebase from "firebase/compat/app";
import FieldValue = firebase.firestore.FieldValue;


@Component({
  selector: 'app-manga',
  templateUrl: './manga.component.html',
  styleUrls: ['./manga.component.css']
})
export class MangaComponent implements OnInit {
  manga = {} as Manga
  capitulos = [];
  cargando = true;
  capitulosPorPagina = 10;
  paginaActual = 1;
  paginas = [] as number[];
  coleccionPaginas = 1;
  user: User | null = null;


  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService,private userService: UserService,
     private firestore: AngularFirestore) {}

  ngOnInit(): void {
    // Recuperar manga de API
    this.route.params.subscribe( (parametros) => {
      const nombre = parametros['name'];
      console.log('Nombre del manga: '+nombre);
      this.mangaAPI.buscarManga(nombre).subscribe( (mangas) => {
        this.manga = mangas[0] as Manga;
        this.obtenerCapitulos();
      });
    });

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

  obtenerCapitulos() {
    this.cargando = true;
    this.mangaAPI.buscarCapitulos(this.manga.chapters_url).subscribe( (capitulos) => {
      console.log(capitulos.body);
      this.capitulos = capitulos.body.reverse();
      this.cargando = false;
      const cantPaginas = this.capitulos.length / this.capitulosPorPagina;
      for (let i = 0; i < cantPaginas; i++) {
        this.paginas.push(i+1);
        console.log(this.paginas);
      }
    });
  }

  descargarEpisodio(episodioURL: string) {
    console.log('descargando: ' + episodioURL);
    console.log(this.manga);
    if (this.user) {
      const docRef = this.firestore.collection('downloads').doc(this.user.uid);
      return docRef.set(
        {
          uid: this.user.uid,
          genres: FieldValue.arrayUnion('action')
        },
        { merge: true }
      );
    } else {
      return;
    }
  }

  verPagina(pagina: number) {
    this.paginaActual = pagina;
  }

  verColeccionPaginas(pagina: number) {
    this.coleccionPaginas = pagina;
    this.verPagina(pagina);
  }

}
