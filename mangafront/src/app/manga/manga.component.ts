import { Component, OnInit, ViewChild } from '@angular/core';
import { Manga, MangaCharacter } from '../interfaces/manga.interface';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { MangaApiService } from '../services/manga-api.service';
import { UserService } from '../services/user.service';
import { User } from 'firebase/auth'; // Importar User de firebase/auth
import { AngularFirestore, AngularFirestoreCollection, QuerySnapshot } from '@angular/fire/compat/firestore';
import firebase from "firebase/compat/app";
import FieldValue = firebase.firestore.FieldValue;
import { MangaModalComponent } from '../manga-modal/manga-modal.component';
import { environment } from 'src/environments/environment';

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
  mangaLinks: any[] = []
  mangaLinksFiltrados: any[] = []
  fuenteActual: any = {}

  mainPlot: Array<MangaCharacter> = []
  additionalCharacters: Array<MangaCharacter> = []

  @ViewChild('mangaModal', { static: false }) mangaModal!: MangaModalComponent;

  userRating = 'Not rated yet';

  inBookmarks = false;
  backend = environment.mainMangaAPI;

  constructor(private router: Router,private route: ActivatedRoute, private mangaAPI: MangaApiService,private userService: UserService,
     private firestore: AngularFirestore) {}

  ngOnInit(): void {
    // Recuperar manga de API
    this.route.queryParams.subscribe( (parametros) => {
      const urlORid = parametros['id'];
      let isnum = /^\d+$/.test(urlORid); // Si no es URL, entonces es una ID de la DB local
      if(isnum) {
        this.mangaAPI.obtenerMangaInfoLocalDB(Number(urlORid)).subscribe( (manga: Manga) => {
          this.manga = manga;
          this.mainPlot = this.manga.characters.filter(c=>c.role=='Main');
          this.additionalCharacters = this.manga.characters.filter(c=>c.role!='Main')
          // Agregar vista a TopMangas
          this.mangaAPI.agregarBusquedaPopular(manga).subscribe(() => {});
          
          
          // Cargar visor de episodios si se selecciono ya uno
          const src = parametros['src'];
          const srcName = parametros['srcName'];
          if(src && srcName) {
            this.obtenerCapitulos(srcName, src);
          } else {
            // Obtener lista de fuentes disponibles de backend
            this.obtenerFuentes();
          }

          // Iniciar sesion
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
      } else {
        const srcInfoName = parametros['srcInfoName'];
        // Guardar, luego cargar
        this.mangaAPI.guardarMangaInfo(urlORid, srcInfoName).subscribe( (manga: Manga) => {
          this.router.navigateByUrl('/manga?id=' + manga.id.toString())
        });
      }

    });

  }

  obtenerFuentes() {
    // Get list of sources retrieved
    this.mangaAPI.obtenerFuentes().subscribe((fuentes: any[]) => {
      let fuentesActivas = []
      for (const f of fuentes) {
        if(f.enabled)
          fuentesActivas.push(f)
      }
      this.fuentes = fuentesActivas;
      
      // Set default source
      this.fuenteActual = this.fuentes[0];
      let fuenteDefault = localStorage.getItem('defaultSrc');
      if(fuenteDefault)
        for (const f of this.fuentes) {
          if(f.name == fuenteDefault)
          this.fuenteActual = f;
        }
      this.mangaAPI.buscarEnFuente(this.fuenteActual.name, this.manga.name).subscribe( (sources: any[]) => {
        // Order by string length (so we mix by similar results to query provided)
        // ASC  -> a.length - b.length
        // DESC -> b.length - a.length
        sources.sort((a, b) => a['name'].length - b['name'].length);
        this.mangaLinks = sources;
        this.mangaLinksFiltrados = this.mangaLinks;
        this.cargando = false;
        this.seleccionandoManga = true;
      });
    });
  }

  filtrarFuentesPorNombre(fuenteNombre: string) {
    if(fuenteNombre == '') {
      this.mangaLinksFiltrados = this.mangaLinks;
    } else {
      this.cargando = true;
      this.seleccionandoManga = false;
      for (const fuente of this.fuentes) {
        if(fuente.name == fuenteNombre)
          this.fuenteActual = fuente;
      }
      this.mangaAPI.buscarEnFuente(this.fuenteActual.name, this.manga.name).subscribe( (sources: any[]) => {
        // Order by string length (so we mix by similar results to query provided)
        // ASC  -> a.length - b.length
        // DESC -> b.length - a.length
        sources.sort((a, b) => a['name'].length - b['name'].length);
        this.mangaLinksFiltrados = sources;
        this.cargando = false;
        this.seleccionandoManga = true;
      });
    }
  }

  regresarAfuentes() {
    window.history.pushState( {} , '', '/manga?id='+this.manga.id );
    this.seleccionandoManga = true;
    if(this.mangaLinksFiltrados.length < 1) {
      this.seleccionandoManga = false;
      this.cargando = true;
      this.obtenerFuentes();
    }
  }

  obtenerCapitulos(fuente_nombre:string, fuente_url: string) {
    window.history.pushState( {} , '', '/manga?id='+this.manga.id+'&'+ new URLSearchParams({srcName: fuente_nombre, src: fuente_url}).toString() );
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
          if(this.manga.id == manga.id) this.inBookmarks = true;
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
