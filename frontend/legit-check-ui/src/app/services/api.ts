import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Product } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000/api'; 

  constructor(private http: HttpClient) { }

  
  checkProduct(code: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/check/${code}/`).pipe(
      catchError(this.handleError)
    );
  }

  login(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login/`, data).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register/`, data).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  addComment(productId: number, text: string): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.post(`${this.apiUrl}/comments/product/${productId}/`, { text }, { headers }).pipe(
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

  deleteComment(commentId: number): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.delete(`${this.apiUrl}/comments/${commentId}/`, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  getAllComments(): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.get(`${this.apiUrl}/all-comments/`, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  getProducts(): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.get(`${this.apiUrl}/products/`, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  addProduct(data: any): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.post(`${this.apiUrl}/products/`, data, { headers }).pipe(
      catchError((error) => throwError(() => error))
    );
  }

  deleteProduct(productId: number): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Token ${token}` };
    return this.http.delete(`${this.apiUrl}/products/${productId}/`, { headers }).pipe(
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
    return throwError(() => new Error(errorMessage));
  }
}