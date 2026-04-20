import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.html',
  styleUrl: './register.scss'
})
export class RegisterComponent {
  registerData = { username: '', password: '', tokenId: '' };
  errorMessage: string = '';

  constructor(private apiService: ApiService, private router: Router) {}

  onRegister() {
    if (this.registerData.tokenId !== 'KBTU-ADMIN-2026') {
      this.errorMessage = 'Неверный Token ID. Доступ запрещен.';
      return;
    }

    this.apiService.register(this.registerData).subscribe({
      next: (response) => {
        localStorage.setItem('token', response.token);
        localStorage.setItem('role', response.role || 'Expert');
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        if (err.error && err.error.error) {
          this.errorMessage = err.error.error;
        } else {
          this.errorMessage = 'Ошибка при регистрации';
        }
      }
    });
  }
}