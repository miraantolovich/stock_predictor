// #region Setup
import { Component, ViewChild } from "@angular/core";
import { ReactiveFormsModule } from '@angular/forms';
import { ApexDataLabels, ApexMarkers, ApexYAxis, NgApexchartsModule } from 'ng-apexcharts';
import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexTitleSubtitle
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis;
  title: ApexTitleSubtitle;
  markers: ApexMarkers;
  dataLabels: ApexDataLabels;
};

@Component({
  selector: "app-stock-chart",
  templateUrl: "./stock-chart.component.html",
  styleUrls: ["./stock-chart.component.css"]
})
//#endregion

export class StockChartComponent {
  // #region Variables
  @ViewChild("chart", { static: false }) chart: ChartComponent;

  protected chart1Options!: Partial<ChartOptions> | any;  
  protected chart2Options!: Partial<ChartOptions> | any;
  protected commonOptions: Partial<ChartOptions> | any;

  protected graphTypes = ["line", "bar", "area"];
  // implement candle later based on data
  protected stockTypes = ["AAPL", "GOOG", "MSFT"];

  protected selectedGraphType = this.graphTypes[0];
  protected selectedStockType = this.stockTypes[0];

  //protected stock_data = [{x: "Jan", y: 10}, {x: "Feb", y: 41}, {x: "Mar", y: 35}, {x: "Apr", y: 51}, {x: "May", y: 49}, {x: "Jun", y: 62}, 
  //                        {x: "Jul", y: 69}, {x: "Aug", y: 91}, {x: "Sep", y: 148}];
  protected stock_data = [10, 41, 35, 51, 49, 62, 69, 91, 148];
  protected x_axis_data = ["Jan", "Feb",  "Mar",  "Apr",  "May",  "Jun",  "Jul",  "Aug", "Sep"]
  protected advanced_data = [10000, 41000, 35000, 51000, 49000, 62000, 69000, 91000, 148000];
  
  // chart 2 should be drop down I think
  protected chart2Types = ["Volume", "RSI", "%R", "SO", "M"];
  protected selectedChart2Type = this.chart2Types[0];

  protected showSMA = false;
  protected showEMA = false;
  protected showBB = false;
  // #endregion

  
  // #region Constructor
  constructor() {  
    this.initCharts()
  }

  public initCharts(): void {
    this.commonOptions = {
      markers: {
        size: 3,
        hover: {
          size: 5
        }
      }
    };

    this.chart1Options = {
      series: [{
        data: this.stock_data,
        name: this.selectedStockType
      }],
      chart: {
        height: 600,
        id: "main",
        type: "line",
        group: "stock"
      },
      xaxis: {
        categories: this.x_axis_data
      },
      yaxis: {
        forceNiceScale: true,
        labels: {
          minWidth: 60,
          maxWidth: 60
        }
      }
    };

    this.chart2Options = {
      series: [
        {
          name: "Volume",
          data: this.advanced_data,
        }
      ],
      chart: {
        toolbar: {
          show: false,
        },  
        id: "advanced",
        group: "stock",
        type: "area",
        height: 200
      },
      dataLabels: {
        enabled: false
      },
      xaxis: {
        categories: this.x_axis_data
      },
      yaxis: {
        forceNiceScale: true,
        labels: {
          minWidth: 60,
          maxWidth: 60
        }
      }
    };
  }
  // #endregion

  // Would it be better for the API to give me the entire data-set for the stock & then I pick and choose what data to display 
  // or would it be better for my API to call only the data I need and then I format it accordingly?
  protected changeChart1() {
    var data_chart1 = []
    
    // line & candle
    if (this.selectedGraphType == "line") {
      console.log("line")
      data_chart1.push({
        data: this.stock_data,
        name: this.selectedStockType
      })
    }
    else {
      console.log("candle")
      data_chart1.push(this.stock_data)
    }

    if (this.showSMA) {
      data_chart1.push({
        name: "SMA",
        data: [10, 25.8333, 23.8889, 32.5185, 37.0123, 45.3372, 52.1124, 70.7408, 104.4939],
        type: "line"
      })
    }

    if (this.showEMA) {
      data_chart1.push({
        name: "EMA",
        data: [10, 25.8333, 23.8889, 32.5185, 37.0123, 45.3372, 52.1124, 70.7408, 104.4939],
        type: "line"
      })
    }

    if (this.showBB) {
      data_chart1.push({
        name: "Lower BB",
        data: [5, 20.8333, 18.8889, 27.5185, 32.0123, 40.3372, 47.1124, 65.7408, 99.4939],
        type: "line"
      })

      data_chart1.push({
        name: "Upper BB",
        data: [20, 35.8333, 33.8889, 42.5185, 47.0123, 55.3372, 62.1124, 80.7408, 114.4939],
        type: "line"
      })

      // https://apexcharts.com/angular-chart-demos/range-area-charts/combo/ why this no work
      /*
      data_chart1.push({   
        type: "rangeArea",       
        name: "BB",
        data: [
          {y: [-2, 4]},
          {x: "Feb", y: [-1, 6]},
          {x: "Mar", y: [3, 10]},
          {x: "Apr", y: [8, 16]},
          {x: "May", y: [13, 22]},
          {x: "Jun", y: [18, 26]},
          {x: "Jul", y: [21, 29]},
          {x: "Aug", y: [21, 28]},
          {x: "Sep", y: [17, 24]}
        ]
      })
      */
    }


    console.log(data_chart1);

    //TODO: FIGURE OUT WHY RANGE AREA CHART IS NOT WORKING??

    this.chart1Options.series = data_chart1;  

    //this.chart1Options.series = data_chart1;
  }
  

  protected changeChart2() {
    var data_chart2 = []

    if (this.selectedChart2Type == "RSI") {
      data_chart2.push({
        name: "RSI",
        data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
        type: "line"
      })
    }

    else if (this.selectedChart2Type == "%R") {
      data_chart2.push({
        name: "%R",
        data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
        type: "line"
      })
    }

    else if (this.selectedChart2Type == "SO") {
      data_chart2.push({
        name: "SO",
        data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
        type: "line"
      })
    }

    else if (this.selectedChart2Type == "M") {
      data_chart2.push({
        name: "Momentum",
        data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
        type: "line"
      })
    }

    //show volume
    else {
      data_chart2.push({
        name: "Volume",
        data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
        type: "area"
      })
    }

    this.chart2Options.series = data_chart2;
  }


  protected updateStockType() {
    console.log("Graph Type: " + this.selectedGraphType)
    console.log("Stock Name: " + this.selectedStockType)

    var data_chart1 = this.changeChart1()
    // do chart 2

    this.chart1Options.series = [{
      data: data_chart1,
      type: this.selectedGraphType
    }];

    this.chart2Options.series = [{
      data: this.advanced_data,
      type: "area"
    }]
  }

  protected updateGraphType() {
    console.log("Graph Type: " + this.selectedGraphType)
    console.log("Stock Name: " + this.selectedStockType)

    this.chart1Options.series = [{
      data: this.stock_data, 
      type: this.selectedGraphType
    }, {
      data: [20, 43, 46, 51, 49, 67, 59, 97, 138], 
      type: "line"
    }];
  }

}
