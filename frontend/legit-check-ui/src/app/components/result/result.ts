import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api'; 
import { Product } from '../../models/product';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './result.html',
  styleUrl: './result.scss'
})
export class ResultComponent implements OnInit {
  product: Product | null = null;
  error: string | null = null;
  loading: boolean = true;
  isExpert: boolean = false;
  newComment: string = '';

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    const code = this.route.snapshot.paramMap.get('code');
    if (!code) {
      this.error = "Код не предоставлен";
      this.loading = false;
      return;
    }

    this.loading = true;

    this.apiService.checkProduct(code).subscribe({
      next: (data) => {
        this.product = data;
        this.loading = false;
        this.isExpert = !!localStorage.getItem('token');
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = "Товар с таким серийным номером не найден или произошла ошибка сервера.";
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  submitComment() {
    if (!this.newComment.trim() || !this.product) return;
    
    this.apiService.addComment(this.product.id, this.newComment).subscribe({
      next: (comment) => {
        if (!this.product!.comments) this.product!.comments = [];
        this.product!.comments.unshift(comment); 
        this.newComment = '';
        this.cdr.detectChanges();
      },
      error: (err) => {
        alert('Ошибка при добавлении комментария. Убедитесь, что вы авторизованы.');
      }
    });
  }
}