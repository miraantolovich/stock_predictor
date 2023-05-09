import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import the FormsModule

import { AppComponent } from './app.component';
import { NgApexchartsModule } from "ng-apexcharts";
import { StockChartComponent } from './stock-chart/stock-chart.component';
import { CheckboxComponent } from './checkbox/checkbox.component';


@NgModule({
  declarations: [
    AppComponent,
    StockChartComponent,
    CheckboxComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    NgApexchartsModule,
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}

