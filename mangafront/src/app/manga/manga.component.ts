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
  seleccionandoManga = false;
  capitulosPorPagina = 10;
  paginaActual = 1;
  paginas = [] as number[];
  coleccionPaginas = 1;
  user: User | null = null;

  fuentes: any[] = []

  // Para el modal
  mostrarModal = false;
  fuenteActual = '';
  tituloActual = '';


  constructor(private route: ActivatedRoute, private mangaAPI: MangaApiService,private userService: UserService,
     private firestore: AngularFirestore) {}

  ngOnInit(): void {
    // Recuperar manga de API
    this.route.queryParams.subscribe( (parametros) => {
      const url = parametros['manga'];
      console.log('Manga URl: '+url);
      this.mangaAPI.obtenerMangaInfo(url).subscribe( (manga) => {
        this.manga = manga;
        this.obtenerFuentes();
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

  obtenerFuentes() {
    this.mangaAPI.encontrarFuentes(this.manga.name).subscribe( (mangas) => {
      this.cargando = false;
      this.seleccionandoManga = true;
      this.fuentes = mangas
    });
  }

  obtenerCapitulos(fuente_url: string) {
    this.seleccionandoManga = false;
    this.cargando = true;
    this.mangaAPI.obtenerCapitulos(fuente_url).subscribe( (capitulos) => {
      console.log(capitulos.body);
      this.capitulos = capitulos.search_items.reverse();
      this.cargando = false;
      const cantPaginas = this.capitulos.length / this.capitulosPorPagina;
      for (let i = 0; i < cantPaginas; i++) {
        this.paginas.push(i+1);
        console.log(this.paginas);
      }
    });
  }

  mostrarEpisodio(titulo: string, episodioURL: string) {
    console.log('descargando: ' + episodioURL);
    this.tituloActual = titulo;
    this.fuenteActual = episodioURL;
    this.mostrarModal = true;
    if (this.user) {
      const docRef = this.firestore.collection('ratings').doc(this.user.uid);
      return docRef.set(
        {
          uid: this.user.uid,
          title: FieldValue.arrayUnion(this.manga.name),
          ratings: FieldValue.arrayUnion(this.manga.statistics.score)
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
