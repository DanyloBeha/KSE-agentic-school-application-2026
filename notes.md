This file is for taking notes, capturing my thought process and developing an idea of what to do and how to do it

## Goal - Time Series Analysis of air raid alerts in Ukraine
1. Get data of air raid alerts
2. Build time series
    1. What on X and Y axes? - hours per day starting from 2022?
    2. What region scope - whole Ukraine?
3. Perform analysis

## Time series analysis
[src](https://www.youtube.com/watch?v=GE3JOFwTWVM)
1. Components
    1. Trend
    2. Seasonality
    3. Cycle (repeating but not seasonal)
    4. Variation (unpredictable - irregularity/noise)
2. Forecasting models
    1. ARIMA model (Auto regressive, integrated moving average)
    2. Exponentian smoothing (for models that doesn't have a clear trend or seasonality) - gives more weight to recent values and less weight to older values + smoothes out the data
3. Implementation
    1. Pandas (pre-process)
        import, manipulate and analyze time series data
    2. Matplotlib (visualize)
        visualize time series data: charts, scatter plots, heatmaps
    Data cleaning, exploratory data analysis, modeling

## Data
I thought about scraping telegram channels, but there is an [api](https://devs.alerts.in.ua/#apiregions_history) for getting history of alerts in all regions, hope it will wor