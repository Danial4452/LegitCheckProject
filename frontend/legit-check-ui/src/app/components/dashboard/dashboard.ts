import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {
  role: string | null = '';
  myComments: any[] = [];
  editingCommentId: number | null = null;
  editingText: string = '';
  loading: boolean = true;
  loadingText: string = 'Подготовка рабочего пространства...';

  constructor(
    private router: Router, 
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }
    this.role = localStorage.getItem('role');
    
    // Искусственная задержка для красивой загрузки (1.5 сек)
    setTimeout(() => {
      this.loadComments();
      this.loading = false;
      this.cdr.detectChanges();
    }, 1500);
  }

  loadComments() {
    this.apiService.getMyComments().subscribe({
      next: (data) => {
        this.myComments = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error("Could not load comments", err)
    });
  }

  startEditing(comment: any) {
    this.editingCommentId = comment.id;
    this.editingText = comment.text;
  }

  cancelEditing() {
    this.editingCommentId = null;
    this.editingText = '';
  }

  saveComment(comment: any) {
    if (!this.editingText.trim()) return;
    this.apiService.updateComment(comment.id, this.editingText).subscribe({
      next: (updated) => {
        comment.text = updated.text;
        this.cancelEditing();
      },
      error: (err) => alert("Ошибка при сохранении комментария")
    });
  }

  logout() {
    this.loadingText = 'Выход из системы...';
    this.loading = true;
    setTimeout(() => {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      // Полная перезагрузка страницы для эффекта "настоящего выхода"
      window.location.href = '/login';
    }, 1500);
  }
}
