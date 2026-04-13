import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule,], 
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home {
  searchCode: string = '';

  constructor(private router: Router) {}

  onCheck() {
    if (this.searchCode.trim()) {
      this.router.navigate(['/check', this.searchCode]);
    }
  }
}