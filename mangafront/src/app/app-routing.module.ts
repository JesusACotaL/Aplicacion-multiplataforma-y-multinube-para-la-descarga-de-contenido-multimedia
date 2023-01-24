import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Router, RouterModule, Routes } from '@angular/router';
import { MangakaComponent } from './mangaka/mangaka.component';
import { HomescreenComponent } from './homescreen/homescreen.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { canActivate,redirectUnauthorizedTo } from '@angular/fire/auth-guard';

const routes: Routes = [
  {path: 'homescreen',component:HomescreenComponent},
  {path:'mangaka/:name', component: MangakaComponent},
  {path: 'login',component: LoginComponent},
  {path: 'register',component: RegisterComponent},
  { path: '', redirectTo: 'homescreen', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 

}
