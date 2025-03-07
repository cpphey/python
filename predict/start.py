import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os


class StockPredictor:
    def __init__(self):
        self.symbols = {'SPX': '^GSPC', 'TSLA': 'TSLA'}
        self.data = self.download_data()

    def download_data(self):
        data = {}
        for symbol, ticker in self.symbols.items():
            # df = yf.download(ticker, start='2020-01-01', end='2025-02-18')
            # df.to_csv(f"data/{symbol}.csv")
            github_username = "abhinavarorags"
            repo_name = "CoolStuff"
            branch_name = "test"
            file_path = f"data/{symbol}.csv"
            url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/{branch_name}/{file_path}"
            print(url)
            df = pd.read_csv(url)
            data[symbol] = df
        return data

    def plot_data(self):
        for symbol, df in self.data.items():
            df['Close'].plot(title=f'{symbol} Closing Prices')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.savefig(f'plots/{symbol}_close.png')
            plt.show()

    def rolling_window_validation(self):
        for symbol, df in self.data.items():
            tscv = TimeSeriesSplit(n_splits=5)
            errors = []
            for train_index, test_index in tscv.split(df['Close']):
                train, test = df['Close'].iloc[train_index], df['Close'].iloc[test_index]
                model = ARIMA(train, order=(5, 1, 0))
                model_fit = model.fit()
                predictions = model_fit.forecast(steps=len(test))
                rmse = np.sqrt(mean_squared_error(test, predictions))
                errors.append(rmse)

            plt.plot(errors, marker='o', linestyle='-', label=f'{symbol} Rolling RMSE')
            plt.xlabel("Split Index")
            plt.ylabel("RMSE")
            plt.title(f"Rolling Window RMSE for {symbol}")
            plt.legend()
            # plt.savefig(f'plots/{symbol}_rolling_rmse.png')
            plt.show()

    def anova_test(self):
        for symbol, df in self.data.items():
            df['returns'] = df['Close'].pct_change().dropna()
            model = sm.OLS(df['returns'].dropna(), sm.add_constant(range(len(df['returns'].dropna())))).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)
            print(f"ANOVA Results for {symbol}:\n{anova_table}\n")

    def arima_forecast(self):
        for symbol in self.data:
            df = self.data[symbol]['Close'].dropna()
            model = ARIMA(df, order=(5, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)
            print(f"ARIMA Prediction for {symbol} on Feb 19: {forecast.iloc[0]:.2f}")

    def lstm_forecast(self):
        for symbol in self.data:
            df = self.data[symbol]['Close'].values.reshape(-1, 1)
            scaler = MinMaxScaler(feature_range=(0, 1))
            df_scaled = scaler.fit_transform(df)

            X_train, y_train = [], []
            lookback = 60
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


if __name__ == "__main__":
    predictor = StockPredictor()
    predictor.plot_data()
    predictor.rolling_window_validation()
    predictor.anova_test()
    # predictor.arima_forecast()
    # predictor.lstm_forecast()
