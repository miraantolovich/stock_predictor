import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiBaseUrl = 'http://localhost:5000/api'; 

  constructor(private http: HttpClient) { }

  getStocks() {
    return this.http.get(`${this.apiBaseUrl}/stock`);
  }

  getPrice(stockId: string) {
    return this.http.get(`${this.apiBaseUrl}/price/${stockId}`);
  }
}
