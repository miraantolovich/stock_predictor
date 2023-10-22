import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import the FormsModule

import { AppComponent } from './app.component';
import { NgApexchartsModule } from "ng-apexcharts";
import { StockChartComponent } from './stock-chart/stock-chart.component';

import { HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [
    AppComponent,
    StockChartComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    NgApexchartsModule,
    HttpClientModule
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}

