// #region Setup
import { Component, ViewChild, OnInit } from "@angular/core";
import { ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../api.service';
import { DatePipe } from '@angular/common';


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
  colors: string[];
};

@Component({
  selector: "app-stock-chart",
  templateUrl: "./stock-chart.component.html",
  styleUrls: ["./stock-chart.component.css"]
})
//#endregion

export class StockChartComponent implements OnInit {
  // #region Variables
  @ViewChild("chart", { static: false }) chart: ChartComponent;

  protected chart1Options!: Partial<ChartOptions> | any;  
  protected chart2Options!: Partial<ChartOptions> | any;
  protected commonOptions: Partial<ChartOptions> | any;

  protected graphTypes = ["line", "candle"];
  // implement candle later based on data
  protected stockTypes = ["AAPL"];

  protected selectedGraphType = this.graphTypes[0];
  protected selectedStockType = this.stockTypes[0];

  protected stock_data = [{x: "Jan", y: 10}, {x: "Feb", y: 41}, {x: "Mar", y: 35}, {x: "Apr", y: 51}, {x: "May", y: 49}, {x: "Jun", y: 62}, 
                          {x: "Jul", y: 69}, {x: "Aug", y: 91}, {x: "Sep", y: 148}];

  protected x_axis_data = ["Jan", "Feb",  "Mar",  "Apr",  "May",  "Jun",  "Jul",  "Aug", "Sep"]
  
  protected volume_data = [10000, 41000, 35000, 51000, 49000, 62000, 69000, 91000, 148000];
  protected roc_data = [1, 2, 3, 0, -3, -2, -4, 1, 0]
  
  protected earningsEstimate = [
    { date: 'Jun 2023', average: '1.19', low: '1.14', high: '1.45' },
    { date: 'Sep 2023', average: '1.36', low: '1.17', high: '1.45'  },
    { date: '2023', average: '5.97', low: '5.43', high: '1.45'  },
    { date: '2024', average: '6.54', low: '5.58', high: '1.45'  },
  ]
  protected revenueEstimate = [
      { date: 'Jun 2023', average: '81.67B', low: '81.67B', high: '81.67B'  },
      { date: 'Sep 2023', average: '90.52B', low: '81.67B', high: '81.67B'  },
      { date: '2023', average: '384.51B', low: '81.67B', high: '81.67B'  },
      { date: '2024', average: '409.11B', low: '81.67B', high: '81.67B'  },
  ]
  protected earningsHistory = [
      { year: '6/29/2022', average: '1.16', actual: '1.2', difference: '0.04'  },
      { year: '9/29/2022', average: '1.16', actual: '1.2', difference: '0.04'  },
      { year: '12/30/2022', average: '1.16', actual: '1.2', difference: '0.04'  },
      { year: '3/30/2023', average: '1.16', actual: '1.2', difference: '0.04'  },
  ]

  protected options_dates = ["May", "June", "July"];
  protected selectedOptionsDate = this.options_dates[0];

  protected options_type = ["Calls", "Puts"];
  protected selectedOptionsType = this.options_type[0];

  protected options_data = [
    {
      strike_price: "150",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    },
    {
      strike_price: "155",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    },
    {
      strike_price: "160",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    }
    ,
    {
      strike_price: "165",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    },
    {
      strike_price: "170",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    },
    {
      strike_price: "175",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    },
    {
      strike_price: "180",
      bid: "182.85",
      ask: "183.25",
      change: "-2.05",
      percent_change: "-1.10%",
      volume: "3",
      open_interest: "4",
      implied_volatility: "395.12%",
    }
  ]

  // chart 2 should be drop down I think
  protected chart2Types = ["Volume", "RSI", "%R", "SO", "ROC"];
  protected selectedChart2Type = this.chart2Types[0];

  protected showSMA = false;
  protected showEMA = false;
  protected showBB = false;

  protected stockColor = "#140f70"
  protected smaColor = "#80A4ED"
  protected emaColor = "#88527F"
  protected bbColor = "#FAC748"

  protected dataLoaded = false
  // #endregion

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.loadDataAndWait();
  }

  loadDataAndWait(): void {
    let dataIsLoaded = false;

    // Fetch your data from the API when the component initializes
    this.apiService.getStocks().subscribe(data => {
      // Process the data and set it to your component properties
      this.stockTypes = data.map(stock => stock.stock_name); // Extract stock names from all items
      // Call any other functions that depend on this data
      console.log(this.stockTypes)
      this.selectedStockType = this.stockTypes[0]
    });
    
    let index = this.stockTypes.indexOf(this.selectedStockType);
    const datePipe = new DatePipe('en-US');
    console.log(index);
        
    this.apiService.getPrice((index + 1).toString()).subscribe(data => {
      this.stock_data = data.map(price => ({
        x: datePipe.transform(new Date(price.date), 'yyyy-MM-dd') || '',
        y: parseFloat(price.adjusted_close_price)
      }));
    
      this.x_axis_data = data.map(price => datePipe.transform(new Date(price.date), 'yyyy-MM-dd') || '');
      this.volume_data = data.map(volume => volume.volume)
    
      console.log(this.stock_data);
      console.log(this.x_axis_data)
    });
    
    this.apiService.getOption((index + 1).toString()).subscribe(data => {

      function convertToDateSimplified(dateString: string) {
        return datePipe.transform(new Date(dateString), 'dd MMM yyyy') || '';
      }
      
      let expirationDates = data.map(item => item.expiration_date);
      const uniqueExpirationDatesSet = new Set(expirationDates);
      const uniqueExpirationDatesArray = Array.from(uniqueExpirationDatesSet);
      const simplifiedDates = uniqueExpirationDatesArray.map(convertToDateSimplified);

      console.log(simplifiedDates);
      this.options_dates = simplifiedDates;
      this.selectedOptionsDate = this.options_dates[0];

      const filteredOptions = data.filter(option => convertToDateSimplified(option.expiration_date) === this.selectedOptionsDate && option.option_type === this.selectedOptionsType.toLowerCase());

      console.log(filteredOptions)

      this.options_data = filteredOptions.map(data => ({
        strike_price: data.strike_price,
        bid: data.bid,
        ask: data.ask,
        change: data.change,
        percent_change: data.percent_change,
        volume: data.volume,
        open_interest: data.open_interest,
        implied_volatility: data.implied_volatility,  
      }));

      console.log(this.options_data)

    });

    this.apiService.getEarningsEstimate((index + 1).toString()).subscribe(data => {
      this.earningsEstimate = data.map(earnings => ({
        date: earnings.date,
        average: earnings.average,
        low: earnings.low,
        high: earnings.high
      }));
    
      console.log(this.earningsEstimate);
    });

    this.apiService.getRevenueEstimate((index + 1).toString()).subscribe(data => {
      this.revenueEstimate = data.map(earnings => ({
        date: earnings.date,
        average: earnings.average,
        low: earnings.low,
        high: earnings.high
      }));
    
      console.log(this.revenueEstimate);
    });

    this.apiService.getEarningsHistory((index + 1).toString()).subscribe(data => {
      this.earningsHistory = data.map(earnings => ({
        year: earnings.year,
        average: earnings.average,
        actual: earnings.actual,
        difference: earnings.difference
      }));
    
      console.log(this.earningsHistory);

    });

    dataIsLoaded = true

    const checkDataInterval = setInterval(() => {
      if (dataIsLoaded) {
        clearInterval(checkDataInterval); // Stop the loop
        this.dataLoaded = true; // Set the dataLoaded flag
        this.initCharts(); // Initialize charts or other actions
      }
    }, 1000); // Check every 1 second
  }

  protected initCharts(): void {
    this.commonOptions = {
    };

    console.log("loading?")
    console.log(this.stock_data)
    this.chart1Options = {
      series: [
        {
          type: "line",
          name: this.selectedStockType,
          data: this.stock_data,
        }
      ],
      chart: {
          height: 450,
          id: "main",
          type: "line",
          group: "stock"
      },
      xaxis: {
        forceNiceScale: true,
        categories: this.x_axis_data
      },
      yaxis: {
        forceNiceScale: true,
        labels: {
          minWidth: 60,
          maxWidth: 60
        }
      },
      colors: [this.stockColor],
    };

    this.chart2Options = {
      series: [
        {
          name: "Volume",
          data: this.volume_data,
        }
      ],
      chart: {
        toolbar: {
          show: false,
        },  
        id: "advanced",
        group: "stock",
        type: "area",
        height: 175
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
    var all_colors = []

    // get stock data just close
    let index = this.stockTypes.indexOf(this.selectedStockType);
    const datePipe = new DatePipe('en-US');
    console.log(index);
    
    console.log("new stock")
    this.apiService.getPrice((index + 1).toString()).subscribe(data => {
      this.stock_data = data.map(price => ({
        x: datePipe.transform(new Date(price.date), 'yyyy-MM-dd') || '',
        y: parseFloat(price.adjusted_close_price)
      }));

      this.x_axis_data = data.map(price => datePipe.transform(new Date(price.date), 'yyyy-MM-dd') || '');

      this.volume_data = data.map(volume => volume.volume);

      console.log(this.stock_data);
      console.log(this.x_axis_data);
      console.log(this.volume_data);
    });

    this.apiService.getIndicator((index + 1).toString()).subscribe(data => {

    });
    
    console.log("line")
    data_line.push({
      data: this.stock_data,
      name: this.selectedStockType
    })
    all_colors.push(this.stockColor);

    let bbData = [{x: "Jan", y: [4, 5]}]
    let smaData = [{x: "Jan", y: 10}]
    let emaData = [{x: "Jan", y: 10}]
    this.apiService.getIndicator((index + 1).toString()).subscribe(data => {
      bbData = data.map(indicator => ({
        x: datePipe.transform(new Date(indicator.date), 'yyyy-MM-dd') || '',
        y: [indicator.bb_lower, indicator.bb_upper].map(val => val || 0)
      }));

      smaData = data.map(indicator => ({
        x: datePipe.transform(new Date(indicator.date), 'yyyy-MM-dd') || '',
        y: indicator.sma || 0
      }));

      emaData = data.map(indicator => ({
        x: datePipe.transform(new Date(indicator.date), 'yyyy-MM-dd') || '',
        y: indicator.ema || 0
      }));

      console.log(bbData)
      console.log(smaData)
      console.log(emaData)
    });


    if (this.showBB) {
      data_line.push({   
          type: "rangeArea",
          name: "BB",
          data: bbData
      })
      all_colors.push(this.bbColor);
    }

    // get options 
    if (this.showSMA) {
      data_line.push({
        name: "SMA",
        data: smaData,
        type: "line"
      })
      all_colors.push(this.smaColor);
    }

    if (this.showEMA) {
      data_line.push({
        name: "EMA",
        data: emaData,
        type: "line"
      })
      all_colors.push(this.emaColor);
    }

    // BB can be rangeArea (change chart to rangeArea, y axis tooltip enabled false)
    if (this.showBB) {
      this.chart1Options = {
        series: data_line,
        chart: {
          height: 450,
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
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4]
        },
        colors: all_colors
      }; 
    }   
    // Otherwise chart is line (change chart to line,  y axis tooltip enabled false)
    else {
      this.chart1Options = {
        series: data_line,
        chart: {
          height: 450,
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
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "straight",
          width: [4, 4, 4, 4, 4, 4]
        },
        colors: all_colors
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
        height: 450,
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
          height: 175
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
          height: 175
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
          height: 175
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

    else if (this.selectedChart2Type == "ROC") {
      this.chart2Options = {
        series: [
          {
            name: "ROC",
            data: this.roc_data,
          }
        ],
        chart: {
          toolbar: {
            show: false,
          },  
          id: "advanced",
          group: "stock",
          type: "line",
          height: 175
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
        },
        annotations: {
          yaxis: [
          {
            y: 0,
            borderColor: "black",
            strokeDashArray: 0,
            borderWidth: 2,
            label: {
              text: "Movement",
              style: {
                color: "#fff",
                background: "black"
              }
            }
          }]
        }

      };  
    }

    //show volume
    else {
      this.chart2Options = {
        series: [
          {
            name: "Volume",
            data: this.volume_data,
          }
        ],
        chart: {
          toolbar: {
            show: false,
          },  
          id: "advanced",
          group: "stock",
          type: "area",
          height: 175
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

  protected updateOptions() {
    console.log("update options");

    this.options_data = [
      {
        strike_price: "155",
        bid: "182.85",
        ask: "183.25",
        change: "-2.05",
        percent_change: "-1.10%",
        volume: "3",
        open_interest: "4",
        implied_volatility: "395.12%",
      },
      {
        strike_price: "160",
        bid: "182.85",
        ask: "183.25",
        change: "-2.05",
        percent_change: "-1.10%",
        volume: "3",
        open_interest: "4",
        implied_volatility: "395.12%",
      },
      {
        strike_price: "165",
        bid: "182.85",
        ask: "183.25",
        change: "-2.05",
        percent_change: "-1.10%",
        volume: "3",
        open_interest: "4",
        implied_volatility: "395.12%",
      }
      ,
      {
        strike_price: "170",
        bid: "182.85",
        ask: "183.25",
        change: "-2.05",
        percent_change: "-1.10%",
        volume: "3",
        open_interest: "4",
        implied_volatility: "395.12%",
      }
    ]
  
  }

  protected updateBothCharts() {

    console.log("New Stock Data");

    this.changeChart1();
    this.changeChart2();
  }

}
