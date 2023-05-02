import { Component } from '@angular/core';


@Component({
  selector: 'app-stock-chart',
  templateUrl: './stock-chart.component.html',
  styleUrls: ['./stock-chart.component.css']
})
export class StockChartComponent {
  selectedStock: string;

  stocks = [
    { name: 'AAPL', label: 'Apple Inc.' },
    { name: 'MSFT', label: 'Microsoft Corporation' },
    { name: 'AMZN', label: 'Amazon.com Inc.' },
    { name: 'GOOG', label: 'Alphabet Inc.' },
    { name: 'FB', label: 'Facebook Inc.' }
  ];

  constructor() {
    this.selectedStock = 'AAPL'; // Initialize the property in the constructor
  }

  onStockSelect(stock: string) {
    this.selectedStock = stock;
    // Call a method to update the stock chart with the selected stock data
  }
}
