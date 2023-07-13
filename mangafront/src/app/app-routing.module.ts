import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Router, RouterModule, Routes } from '@angular/router';
import { MangakaComponent } from './mangaka/mangaka.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { canActivate,redirectUnauthorizedTo } from '@angular/fire/auth-guard';
import { HomeComponent } from './home/home.component';
import { BuscarComponent } from './buscar/buscar.component';
import { MangaComponent } from './manga/manga.component';
import { PerfilComponent } from './perfil/perfil.component';
import { MangaModalComponent } from './manga-modal/manga-modal.component';

const routes: Routes = [
  {path:'', redirectTo: 'home', pathMatch: 'full' },
  {path:'home',component:HomeComponent},
  {path:'buscar/:name',component:BuscarComponent},
  {path:'manga',component:MangaComponent},
  {path:'manga-modal',component:MangaModalComponent},
  {path:'mangaka/:name', component: MangakaComponent},
  {path:'login',component: LoginComponent},
  {path:'register',component: RegisterComponent},
  {path:'user',component:PerfilComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 
  
}
