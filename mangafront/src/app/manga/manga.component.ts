import { Component, OnInit } from '@angular/core';
import { Manga } from '../interfaces/manga.interface';
import { ActivatedRoute } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { AngularFirestore, AngularFirestoreCollection, QuerySnapshot } from '@angular/fire/compat/firestore';
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
  myanimelisturl = '';
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
      this.myanimelisturl = url;
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

  getMainPlot() {
    if(this.manga.characters)
    return this.manga.characters.filter(c=>c.role=='Main');
    else
    return []
  }

  getAdditionalCharacters() {
    if(this.manga.characters)
    return this.manga.characters.filter(c=>c.role!='Main')
    else
    return []
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
      this.capitulos = capitulos.search_items.reverse();
      this.cargando = false;
      const cantPaginas = this.capitulos.length / this.capitulosPorPagina;
      for (let i = 0; i < cantPaginas; i++) {
        this.paginas.push(i+1);
      }
    });
  }

  mostrarEpisodio(titulo: string, episodioURL: string) {
    this.tituloActual = titulo;
    this.fuenteActual = episodioURL;
    this.mostrarModal = true;
  }

  verPagina(pagina: number) {
    this.paginaActual = pagina;
  }

  verColeccionPaginas(pagina: number) {
    this.coleccionPaginas = pagina;
    this.verPagina(pagina);
  }

  rate(value: number) {
    if (this.user) {
      const uid = this.user?.uid;
      const title = this.manga.name;
      this.mangaAPI.calificarManga(uid, title, value.toString()).subscribe(()=>{})
    } else {
      return;
    }
  }

}
