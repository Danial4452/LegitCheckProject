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
  username: string | null = '';
  isAdmin: boolean = false;
  myComments: any[] = [];
  allComments: any[] = [];
  products: any[] = [];
  
  activeTab: 'my-comments' | 'all-comments' | 'products' = 'my-comments';

  editingCommentId: number | null = null;
  editingText: string = '';
  loading: boolean = true;
  loadingText: string = 'Подготовка рабочего пространства...';

  // For adding a product
  newProduct = {
    name: '', brand: '', serial_number: '', manufacture_location: '', history: '', is_authentic: true
  };

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
    this.username = localStorage.getItem('username') || 'Пользователь';
    this.isAdmin = localStorage.getItem('isAdmin') === 'true';
    
    // Искусственная задержка для красивой загрузки (1.5 сек)
    setTimeout(() => {
      this.loadMyComments();
      if (this.isAdmin) {
        this.loadAllComments();
        this.loadProducts();
      }
      this.loading = false;
      this.cdr.detectChanges();
    }, 1500);
  }

  setTab(tab: 'my-comments' | 'all-comments' | 'products') {
    this.activeTab = tab;
  }

  loadMyComments() {
    this.apiService.getMyComments().subscribe({
      next: (data) => {
        this.myComments = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error("Could not load comments", err)
    });
  }

  loadAllComments() {
    this.apiService.getAllComments().subscribe({
      next: (data) => {
        this.allComments = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error("Could not load all comments", err)
    });
  }

  loadProducts() {
    this.apiService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error("Could not load products", err)
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

  deleteComment(id: number) {
    if (confirm('Вы уверены, что хотите удалить этот комментарий?')) {
      this.apiService.deleteComment(id).subscribe({
        next: () => {
          this.allComments = this.allComments.filter(c => c.id !== id);
          this.myComments = this.myComments.filter(c => c.id !== id);
          this.cdr.detectChanges();
        },
        error: (err) => alert("Ошибка при удалении комментария")
      });
    }
  }

  addProduct() {
    if (!this.newProduct.name || !this.newProduct.brand || !this.newProduct.serial_number) {
      alert('Заполните обязательные поля');
      return;
    }
    this.apiService.addProduct(this.newProduct).subscribe({
      next: (prod) => {
        this.products.unshift(prod);
        this.newProduct = { name: '', brand: '', serial_number: '', manufacture_location: '', history: '', is_authentic: true };
        this.cdr.detectChanges();
        alert('Товар успешно добавлен!');
      },
      error: (err) => alert("Ошибка при добавлении товара")
    });
  }

  deleteProduct(id: number) {
    if (confirm('Вы уверены, что хотите удалить этот товар?')) {
      this.apiService.deleteProduct(id).subscribe({
        next: () => {
          this.products = this.products.filter(p => p.id !== id);
          this.cdr.detectChanges();
        },
        error: (err) => alert("Ошибка при удалении товара")
      });
    }
  }

  logout() {
    this.loadingText = 'Выход из системы...';
    this.loading = true;
    setTimeout(() => {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      localStorage.removeItem('isAdmin');
      window.location.href = '/login';
    }, 1500);
  }
}
