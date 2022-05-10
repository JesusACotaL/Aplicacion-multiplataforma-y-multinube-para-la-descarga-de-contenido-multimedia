import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Router, RouterModule, Routes } from '@angular/router';
import { MangakaComponent } from './mangaka/mangaka.component';
import { HomescreenComponent } from './homescreen/homescreen.component';


const routes: Routes = [
  {path: 'homescreen',component:HomescreenComponent},
  {path:'mangaka/:name', component: MangakaComponent},
  { path: '', redirectTo: 'homescreen', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 

}
