import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Router, RouterModule, Routes } from '@angular/router';
import { MangakaComponent } from './mangaka/mangaka.component';
import { HomescreenComponent } from './homescreen/homescreen.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { canActivate,redirectUnauthorizedTo } from '@angular/fire/auth-guard';
import { HomeComponent } from './home/home.component';
import { BuscarComponent } from './buscar/buscar.component';
import { MangaComponent } from './manga/manga.component';
import { PerfilComponent } from './perfil/perfil.component';
import { PruebasAPIComponent } from './pruebas-api/pruebas-api.component';

const routes: Routes = [
  {path:'', redirectTo: 'home', pathMatch: 'full' },
  {path:'home',component:HomeComponent},
  {path:'pruebasAPI',component:PruebasAPIComponent},
  {path:'buscar/:name',component:BuscarComponent},
  {path:'manga/:name',component:MangaComponent},
  {path:'homescreen',component:HomescreenComponent},
  {path:'mangaka/:name', component: MangakaComponent},
  {path:'login',component: LoginComponent},
  {path:'register',component: RegisterComponent},
  {path:'perfil',component:PerfilComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 
  
}
