import { Component} from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'mangafront';

  constructor(private router: Router) { }

  get_mangas_urls(): void{
    let nombre_manga = ((document.getElementById("buscador_manga") as HTMLInputElement).value);
    console.log(nombre_manga)
    this.router.navigateByUrl('/mangaka')
  }
}


