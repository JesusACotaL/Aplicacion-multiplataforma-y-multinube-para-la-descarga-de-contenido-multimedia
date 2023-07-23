import { Component, OnInit, ViewChild } from '@angular/core';
import { Manga } from '../interfaces/manga.interface';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { AngularFirestore, AngularFirestoreCollection, QuerySnapshot } from '@angular/fire/compat/firestore';
import firebase from "firebase/compat/app";
import FieldValue = firebase.firestore.FieldValue;
import { MangaModalComponent } from '../manga-modal/manga-modal.component';


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
  capitulosPorPagina = 6;
  paginaActual = 1;
  paginas = [] as number[];
  coleccionPaginas = 1;
  user: User | null = null;
  chapQuery = '';
  filtrados: any[] = [];

  fuentes: any[] = []
  myanimelisturl = '';

  @ViewChild('mangaModal', { static: false }) mangaModal!: MangaModalComponent;

  userRating = 'Not rated yet';

  inBookmarks = false;

  constructor(private router: Router,private route: ActivatedRoute, private mangaAPI: MangaApiService,private userService: UserService,
     private firestore: AngularFirestore) {}

  ngOnInit(): void {
    // Recuperar manga de API
    this.route.queryParams.subscribe( (parametros) => {
      const url = parametros['manga'];
      this.myanimelisturl = url;
      this.mangaAPI.obtenerMangaInfo(url).subscribe( (manga: Manga) => {
        this.manga = manga;
        // Agregar vista a TopMangas
        this.mangaAPI.agregarBusquedaPopular(manga).subscribe(() => {});

        this.obtenerFuentes();
        this.userService.getAuth().onAuthStateChanged((user) => {
          if (user) {
            // User is signed in, see docs for a list of available properties
            // https://firebase.google.com/docs/reference/js/firebase.User
            this.user = user;
            this.getRating();
            this.checkIfInBookmarks();
          } else {
            // User is signed out
          }
        });
      });
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

  obtenerCapitulos(fuente_nombre:string, fuente_url: string) {
    this.seleccionandoManga = false;
    this.cargando = true;
    this.mangaAPI.obtenerCapitulos(fuente_nombre,fuente_url).subscribe( (capitulos) => {
      this.capitulos = capitulos;
      this.filtrados = this.capitulos;
      this.cargando = false;
      const cantPaginas = this.capitulos.length / this.capitulosPorPagina;
      for (let i = 0; i < cantPaginas; i++) {
        this.paginas.push(i+1);
      }
    });
  }

  filterChapters() {
    this.paginas = []
    const cantPaginas = this.filtrados.length / this.capitulosPorPagina;
    for (let i = 0; i < cantPaginas; i++) {
      this.paginas.push(i+1);
    }
    if(this.chapQuery != '') {
      this.filtrados = this.capitulos.filter( (element: any) => element['name'].toLowerCase().search(this.chapQuery.toLowerCase()) != -1);
    } else {
      this.filtrados = this.capitulos;
    }
  }

  mostrarEpisodio(titulo: string, episodioURL: string, fuenteNombre: string) {
    const queryParams: Params = { chap: episodioURL, title: titulo, chapSrcName: fuenteNombre };
    if(this.user) {
      this.userService.addToHistory(this.user.uid, this.manga).subscribe( () => {});
    }
    this.mangaModal.mostrar(titulo, fuenteNombre, episodioURL);
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
      this.userService.rateManga(uid, title, value.toString()).subscribe((data)=>{
        this.getRating()
      })
    } else {
      return;
    }
  }

  getRating() {
    const uid = this.user?.uid;
    const title = this.manga.name;
    this.userService.getMangaRating(uid!, title).subscribe((result)=>{
      if(result) {
        this.userRating = result['rating'].toString();
        const radio1 = document.getElementById('radio1') as HTMLInputElement | null;
        const radio2 = document.getElementById('radio2') as HTMLInputElement | null;
        const radio3 = document.getElementById('radio3') as HTMLInputElement | null;
        const radio4 = document.getElementById('radio4') as HTMLInputElement | null;
        const radio5 = document.getElementById('radio5') as HTMLInputElement | null;
        switch (result['rating']) {
          case 1:
            radio1!.checked = true;
            break;
          case 2:
            radio2!.checked = true;
            break;
          case 3:
            radio3!.checked = true;
            break;
          case 4:
            radio4!.checked = true;
            break;
          case 5:
            radio5!.checked = true;
            break;
        
          default:
            break;
        }
      } else {
        this.userRating = 'Not rated yet.'
      }
    })
  }

  checkIfInBookmarks() {
    if(this.user && this.manga.name) {
      this.userService.getBookmarks(this.user.uid).subscribe((bookmarks: Array<Manga>) => {
        for (const manga of bookmarks) {
          if(this.manga.mangaID == manga.mangaID) this.inBookmarks = true;
        }
      });
    }
  }

  addToBookmarks() {
    if(this.user && this.manga.name) {
      this.userService.addMangaToBookmarks(this.user.uid,this.manga).subscribe(() => {
        this.inBookmarks = true;
      });
    }
  }

  removeFromBookmarks() {
    if(this.user && this.manga.name) {
      this.userService.removeMangaFromBookmarks(this.user.uid,this.manga).subscribe(() => {
        this.inBookmarks = false;
      });
    }
  }

}
