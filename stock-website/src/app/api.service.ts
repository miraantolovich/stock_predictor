import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


// INTERFACES FOR DATA
export interface IStock {
  stock_id: number;
  stock_long_name: string;
  stock_name: string;
}

export interface IPrice {
  adjusted_close_price: string;
  close_price: string;
  date: string;
  high_price: string;
  low_price: string;
  open_price: string;
  percent_change: string | null;
  stock_id: number;
  volume: number;
}

export interface IIndicator {
  bb_lower: number | null;
  bb_middle: number | null;
  bb_upper: number | null;
  date: string;
  ema: number;
  r_percent: number | null;
  roc: number | null;
  rsi: number | null;
  si_d: number | null;
  si_k: number | null;
  sma: number | null;
  stock_id: number;
}

export interface IOption {
  ask: string;
  bid: string;
  change: string;
  date: string;
  expiration_date: string;
  implied_volatility: string;
  open_interest: string;
  option_type: string;
  percent_change: string;
  stock_id: number;
  strike_price: string;
  volume: string;
}

export interface IEarningsEstimate {
  date: string;
  average: string;
  low: string;
  high: string;
}

export interface IEarningsHistory {
  year: string;
  average: string;
  actual: string;
  difference: string;
}

export interface IRevenueEstimate {
  date: string;
  average: string;
  low: string;
  high: string;
}



@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiBaseUrl = 'http://127.0.0.1:5000/api'; 

  constructor(private http: HttpClient) { }

  getStocks(): Observable<IStock[]> {
    return this.http.get<IStock[]>(`${this.apiBaseUrl}/stock`);
  }

  getPrice(stockId: string) {
    return this.http.get<IPrice[]>(`${this.apiBaseUrl}/price/${stockId}`);
  }

  getIndicator(stockId: string) {
    return this.http.get<IIndicator[]>(`${this.apiBaseUrl}/indicator/${stockId}`);
  }

  getOption(stockId: string) {
    return this.http.get<IOption[]>(`${this.apiBaseUrl}/option/${stockId}`);
  }

  getEarningsEstimate(stockId: string) {
    return this.http.get<IEarningsEstimate[]>(`${this.apiBaseUrl}/earningsestimate/${stockId}`);
  }

  getEarningsHistory(stockId: string) {
    return this.http.get<IEarningsHistory[]>(`${this.apiBaseUrl}/earningshistory/${stockId}`);
  }

  getRevenueEstimate(stockId: string) {
    return this.http.get<IRevenueEstimate[]>(`${this.apiBaseUrl}/revenueestimate/${stockId}`);
  }


}
