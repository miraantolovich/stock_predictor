// #region Setup
import { Component, ViewChild } from "@angular/core";
import { ReactiveFormsModule } from '@angular/forms';
import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexChart,
  ApexTitleSubtitle,
  ApexXAxis,
  ApexDataLabels,
  ApexStroke,
  ApexYAxis,
  ApexMarkers,
  ApexAnnotations,
  ApexFill,
  ApexForecastDataPoints,
  ApexLegend
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis;
  title: ApexTitleSubtitle;
  stroke: ApexStroke;
  markers: ApexMarkers;
  dataLabels: ApexDataLabels;
  annotations: ApexAnnotations;
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

  protected graphTypes = ["line", "candle"];
  // implement candle later based on data
  protected stockTypes = ["AAPL", "GOOG", "MSFT"];

  protected selectedGraphType = this.graphTypes[0];
  protected selectedStockType = this.stockTypes[0];

  protected stock_data = [{x: "Jan", y: 10}, {x: "Feb", y: 41}, {x: "Mar", y: 35}, {x: "Apr", y: 51}, {x: "May", y: 49}, {x: "Jun", y: 62}, 
                          {x: "Jul", y: 69}, {x: "Aug", y: 91}, {x: "Sep", y: 148}];
  //protected stock_data = [10, 41, 35, 51, 49, 62, 69, 91, 148];
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
      series: [
        {
          type: "line",
          name: this.selectedStockType,
          data: this.stock_data
        }
      ],
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
        height: 250
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
      },
      stroke: {
        curve: "straight",
        width: [4, 4, 4, 4, 4, 4],
      }
    };
  }
  // #endregion


  // Would it be better for the API to give me the entire data-set for the stock & then I pick and choose what data to display 
  // or would it be better for my API to call only the data I need and then I format it accordingly?
  protected changeChart1() {    
    // line
    if (this.selectedGraphType == "line") {
      this.ifLine();
    }
    // candle
    else if (this.selectedGraphType == "candle") {
      this.showSMA = false;
      this.showEMA = false;
      this.showBB = false;

      this.ifCandle();
    }
    else {
      console.log("This shouldn't be possible! Error!");  
    }
  }
  

  private ifLine() {
    var data_line = []
    // get stock data just close
    console.log("line")
    data_line.push({
      data: this.stock_data,
      name: this.selectedStockType
    })

    // get options 
    if (this.showSMA) {
      data_line.push({
        name: "SMA",
        data: [{x: "Jan", y: 10}, {x: "Feb", y: 30}, {x: "Mar", y: 20}, {x: "Apr", y: 30}, 
               {x: "May", y: 20}, {x: "Jun", y: 45}, {x: "Jul", y: 68}, {x: "Aug", y: 57}, {x: "Sep", y: 78}],
        type: "line"
      })
    }

    if (this.showEMA) {
      data_line.push({
        name: "EMA",
        data: [{x: "Jan", y: 10}, {x: "Feb", y: 25.8333}, {x: "Mar", y: 23.8889}, {x: "Apr", y: 32.5185}, 
               {x: "May", y: 37.0123}, {x: "Jun", y: 45.3372}, {x: "Jul", y: 52.1124}, {x: "Aug", y: 70.7408}, {x: "Sep", y: 104.4939}],
        type: "line"
      })
    }

    if (this.showBB) {
      data_line.push({   
          type: "rangeArea",
          name: "BB",
          data: [
            {x: "Jan", y: [4, 5]},
            {x: "Feb", y: [20, 25]},
            {x: "Mar", y: [3, 10]},
            {x: "Apr", y: [8, 16]},
            {x: "May", y: [13, 22]},
            {x: "Jun", y: [18, 26]},
            {x: "Jul", y: [21, 29]},
            {x: "Aug", y: [21, 28]},
            {x: "Sep", y: [17, 24]}
          ]
      })
    }


    // BB can be rangeArea (change chart to rangeArea, y axis tooltip enabled false)
    if (this.showBB) {
      this.chart1Options = {
        series: data_line,
        chart: {
          height: 600,
          id: "main",
          type: "rangeArea",
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
          },
          tooltip: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4]
        }
      }; 
    }   
    // Otherwise chart is line (change chart to line,  y axis tooltip enabled false)
    else {
      this.chart1Options = {
        series: data_line,
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
          },
          tooltip: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4]
        }
      }; 
    }


  }

  private ifCandle() {
    var data_candle = []
    // get stock data open, high, low, close
    console.log("candle")
    data_candle.push({
      type: "candlestick",
      data: [
        {x: "Jan", y: [4, 5, 3, 4]},
        {x: "Feb", y: [20, 25, 10, 14]},
        {x: "Mar", y: [3, 10, 4, 5]},
        {x: "Apr", y: [8, 16, 6, 10]},
        {x: "May", y: [13, 22, 14, 20]},
        {x: "Jun", y: [18, 26, 19, 21]},
        {x: "Jul", y: [21, 29, 21, 24]},
        {x: "Aug", y: [21, 28, 18, 18]},
        {x: "Sep", y: [17, 24, 19, 23]}
      ],
      name: this.selectedStockType
    })

    // Chart has to be candlestick (change chart to candlestick)
    // y axis tooltip enabled (true)
    this.chart1Options = {
      series: data_candle,
      chart: {
        height: 600,
        id: "main",
        type: "candlestick",
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
        },
        tooltip: {
          enabled: true
        }
      },
      stroke: {
        curve: "straight",
        width: [4, 4, 4, 4, 4, 4],
      }
    }; 
  }


  protected changeChart2() {
    var data_chart2 = []

    if (this.selectedChart2Type == "RSI") {
      this.chart2Options = {
        series: [
          {
            name: "RSI",
            data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
          }
        ],
        chart: {
          toolbar: {
            show: false,
          },  
          id: "advanced",
          group: "stock",
          type: "line",
          height: 250
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: this.x_axis_data
        },
        yaxis: {
          labels: {
            minWidth: 60,
            maxWidth: 60
          },
          min: 0,
          max: 100  
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4],
        },
        annotations: {
          yaxis: [
          {
            y: 30,
            borderColor: "green",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Oversold",
              style: {
                color: "#fff",
                background: "green"
              }
            }
          },
          {
            y: 70,
            borderColor: "red",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Overbought",
              style: {
                color: "#fff",
                background: "red"
              }
            }
          }
        ]
        }
      }
    } 

    else if (this.selectedChart2Type == "%R") {
      this.chart2Options = {
        series: [
          {
            name: "%R",
            data: [-10, -30, -20, -30, -20, -45, -68, -57, -78]
          }
        ],
        chart: {
          toolbar: {
            show: false,
          },  
          id: "advanced",
          group: "stock",
          type: "line",
          height: 250
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: this.x_axis_data
        },
        yaxis: {
          labels: {
            minWidth: 60,
            maxWidth: 60
          },
          min: -100,
          max: 0  
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4],
        },
        annotations: {
          yaxis: [
          {
            y: -20,
            borderColor: "red",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Overbought",
              style: {
                color: "#fff",
                background: "red"
              }
            }
          },
          {
            y: -80,
            borderColor: "green",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Oversold",
              style: {
                color: "#fff",
                background: "green"
              }
            }
          }
        ]
        }
      }
    }

    else if (this.selectedChart2Type == "SO") {
      this.chart2Options = {
        series: [
          {
            name: "SO",
            data: [10, 30, 20, 30, 20, 45, 68, 57, 78],
          }
          // add %K & %D
        ],
        chart: {
          toolbar: {
            show: false,
          },  
          id: "advanced",
          group: "stock",
          type: "line",
          height: 250
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: this.x_axis_data
        },
        yaxis: {
          labels: {
            minWidth: 60,
            maxWidth: 60
          },
          min: 0,
          max: 100  
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4],
        },
        annotations: {
          yaxis: [
          {
            y: 20,
            borderColor: "green",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Oversold",
              style: {
                color: "#fff",
                background: "green"
              }
            }
          },
          {
            y: 80,
            borderColor: "red",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Overbought",
              style: {
                color: "#fff",
                background: "red"
              }
            }
          }
        ]
        }
      }
    }

    else if (this.selectedChart2Type == "Momentum") {
      this.chart2Options = {
        series: [
          {
            name: "Momentum",
            data: this.advanced_data,
          }
        ],
        chart: {
          toolbar: {
            show: false,
          },  
          id: "advanced",
          group: "stock",
          type: "line",
          height: 250
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
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4],
        }
      };  
    }

    //show volume
    else {
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
          height: 250
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
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4],
        }
      };  
    }
    
  }


  protected updateBothCharts() {

    console.log("New Stock Data");

    this.changeChart1();
    this.changeChart2();
  }

}
