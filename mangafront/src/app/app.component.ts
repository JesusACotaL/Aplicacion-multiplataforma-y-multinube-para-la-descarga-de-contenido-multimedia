import { Component} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'mangafront';

  get_mangas_urls(): void{
    let nombre_manga = ((document.getElementById("buscador_manga") as HTMLInputElement).value);
    
    console.log(nombre_manga)
  }
}


