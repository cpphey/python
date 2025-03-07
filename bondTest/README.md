# Stock Price Prediction

This script predicts the closing prices of SPX and TSLA using multiple forecasting models:
- **ARIMA** (Time Series Model)
- **Random Forest** (Machine Learning Model)
- **XGBoost** (Gradient Boosting Model)

## Features:
- Downloads historical stock data
- Performs data visualization
- Forecasts future closing prices
- Evaluates model performance with rolling window validation
- Conducts stationarity tests using the Augmented Dickey-Fuller test

## Usage:
Run the script to generate predictions and validation results. The models use historical price data with lag features for training and inference.

