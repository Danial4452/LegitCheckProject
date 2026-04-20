import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Product } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000/api'; // Адрес Django твоего напарника

  constructor(private http: HttpClient) { }

  // Метод для проверки кода
  checkProduct(code: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/check/${code}/`).pipe(
      catchError(this.handleError) // Requirement 9: Graceful error handling
    );
  }

  login(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/login/`, data).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, data).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  addComment(productId: number, text: string): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.post(`${this.apiUrl}/products/${productId}/comments/`, { text }, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  getMyComments(): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.get(`${this.apiUrl}/my-comments/`, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  updateComment(commentId: number, text: string): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.put(`${this.apiUrl}/comments/${commentId}/`, { text }, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Произошла неизвестная ошибка';
    if (error.status === 404) {
      errorMessage = 'Товар с таким кодом не найден в базе данных.';
    } else if (error.status === 500) {
      errorMessage = 'Ошибка на стороне сервера. Попробуйте позже.';
    }
    // Здесь можно выводить ошибку в консоль или алертом
    return throwError(() => new Error(errorMessage));
  }
}