import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


class StockPredictor:
    def __init__(self):
        self.symbols = {'SPX': '^GSPC', 'TSLA': 'TSLA'}
        self.data = self.download_data()

    def download_data(self):
        data = {}
        for symbol, ticker in self.symbols.items():
            data[symbol] = yf.download(ticker, start='2020-01-01', end='2025-02-18')
        return data

    def arima_forecast(self):
        for symbol in self.data:
            df = self.data[symbol]['Close'].dropna()
            model = ARIMA(df, order=(5, 1, 0))  # ARIMA order (p,d,q)
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)
            print(f"ARIMA Prediction for {symbol} on Feb 19: {forecast.iloc[0]:.2f}")

    def lstm_forecast(self):
        for symbol in self.data:
            df = self.data[symbol]['Close'].values.reshape(-1, 1)
            scaler = MinMaxScaler(feature_range=(0, 1))
            df_scaled = scaler.fit_transform(df)

            X_train, y_train = [], []
            lookback = 60  # Use last 60 days to predict next day
            for i in range(lookback, len(df_scaled)):
                X_train.append(df_scaled[i - lookback:i, 0])
                y_train.append(df_scaled[i, 0])
            X_train, y_train = np.array(X_train), np.array(y_train)
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                LSTM(50, return_sequences=False),
                Dense(25),
                Dense(1)
            ])

            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(X_train, y_train, batch_size=1, epochs=5, verbose=0)

            test_input = df_scaled[-lookback:].reshape(1, lookback, 1)
            prediction = model.predict(test_input)
            prediction = scaler.inverse_transform(prediction)

            print(f"LSTM Prediction for {symbol} on Feb 19: {prediction[0][0]:.2f}")

def main():
    predictor = StockPredictor()
    predictor.arima_forecast()
    predictor.lstm_forecast()

if __name__ == "__main__":
    main()