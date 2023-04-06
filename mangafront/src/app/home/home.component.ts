import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  // Como funcionan los template-driven forms: https://angular.io/guide/forms#summary
  manga = '';

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  buscar() {
    this.router.navigate(['/buscar',this.manga]);
  }

}
