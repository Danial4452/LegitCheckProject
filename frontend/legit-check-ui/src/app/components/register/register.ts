import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

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

  constructor(private router: Router) {}

  onRegister() {
    // Пример токена для KBTU
    if (this.registerData.tokenId === 'KBTU-ADMIN-2026') {
      console.log('Данные регистрации:', this.registerData);
      this.router.navigate(['/login']);
    } else {
      this.errorMessage = 'Неверный Token ID. Доступ запрещен.';
    }
  }
}