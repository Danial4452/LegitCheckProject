
import { ResultComponent } from './components/result/result'; 
import { Home } from './components/home/home';
import { LoginComponent } from './components/login/login';
import { Routes } from '@angular/router';
import { RegisterComponent } from './components/register/register';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'check/:code', component: ResultComponent }, 
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: '**', redirectTo: '' }
];