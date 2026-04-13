import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule], // Обязательно для ngModel
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class LoginComponent {
  loginData = {
    username: '',
    password: ''
  };
  errorMessage: string = '';

  constructor(private apiService: ApiService, private router: Router) {}

  onLogin() {
    console.log('Данные для входа:', this.loginData);
    
    // Пока бэкенд не готов, сделаем проверку "для вида"
    if (this.loginData.username === 'admin' && this.loginData.password === '12345') {
      localStorage.setItem('token', 'fake-jwt-token'); // Имитация JWT
      this.router.navigate(['/']); // Возвращаемся на главную
    } else {
      this.errorMessage = 'Неверный логин или пароль';
    }
  }
}