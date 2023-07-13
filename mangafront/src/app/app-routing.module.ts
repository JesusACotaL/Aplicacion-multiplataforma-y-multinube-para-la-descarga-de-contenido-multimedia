import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Router, RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { canActivate,redirectUnauthorizedTo } from '@angular/fire/auth-guard';
import { HomeComponent } from './home/home.component';
import { SearchComponent } from './search/search.component';
import { MangaComponent } from './manga/manga.component';
import { AccountComponent } from './account/account.component';
import { MangaModalComponent } from './manga-modal/manga-modal.component';
import { NavbarComponent } from './navbar/navbar.component';

const routes: Routes = [
  {path:'', redirectTo: 'home', pathMatch: 'full' },
  {path:'home',component:HomeComponent},
  {path:'search/:name',component:SearchComponent},
  {path:'manga',component:MangaComponent},
  {path:'manga-modal',component:MangaModalComponent},
  {path:'login',component: LoginComponent},
  {path:'register',component: RegisterComponent},
  {path:'account',component:AccountComponent},
  {path:'navbar',component:NavbarComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 
  
}
