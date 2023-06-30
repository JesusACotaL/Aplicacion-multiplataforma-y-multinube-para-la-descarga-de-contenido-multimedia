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
      const title = this.manga.name;
      const ratingsCollection: AngularFirestoreCollection<any> = this.firestore.collection('ratings');
  
      // Realizar la consulta para verificar si el título ya existe
      return ratingsCollection.ref.where('title', '==', title).get().then((querySnapshot: QuerySnapshot<any>) => {
        if (querySnapshot.empty) {
          // No hay documentos que coincidan con el título, agregarlo
          return ratingsCollection.add({
            uid: this.user?.uid, // Navegación segura para acceder a this.user.uid
            title: title,
            ratings: this.manga.statistics.score
          });
        } else {
          // El título ya existe, no hacer nada
          return;
        }
      });
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
