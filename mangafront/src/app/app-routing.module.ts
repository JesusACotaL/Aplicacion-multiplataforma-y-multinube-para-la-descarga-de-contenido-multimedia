import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Router, RouterModule, Routes } from '@angular/router';
import { canActivate,redirectUnauthorizedTo } from '@angular/fire/auth-guard';
import { HomeComponent } from './home/home.component';
import { SearchComponent } from './search/search.component';
import { MangaComponent } from './manga/manga.component';
import { GenreComponent } from './genre/genre.component';

const routes: Routes = [
  {path:'', redirectTo: 'home', pathMatch: 'full' },
  {path:'home',component:HomeComponent},
  {path:'search/:name',component:SearchComponent},
  {path:'genre/:name',component:GenreComponent},
  {path:'manga',component:MangaComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 
  
}
