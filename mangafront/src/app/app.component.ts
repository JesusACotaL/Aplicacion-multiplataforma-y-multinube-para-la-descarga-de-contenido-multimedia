import { Component} from '@angular/core';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'mangafront';

  constructor(private router: Router) { }

  getCurrentRoute(): string {
    return this.router.url
  }

}


