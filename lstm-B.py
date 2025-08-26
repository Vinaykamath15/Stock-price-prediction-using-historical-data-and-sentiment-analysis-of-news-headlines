import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping

hist_df = pd.read_csv('/kaggle/input/combined-stock-data/combined_nifty_fii_dii_vix.csv')
hist_df['Date'] = pd.to_datetime(hist_df['Date'], format='%d-%m-%Y')
hist_df.drop(columns=['Index Name'], errors='ignore', inplace=True)
hist_df.sort_values('Date', inplace=True)


news_df = pd.read_csv('/kaggle/input/financial-news/financial_news.csv')
news_df['Date'] = pd.to_datetime(news_df['Date'], format='%d/%m/%y')
news_df['confidence'] = pd.to_numeric(news_df['confidence'], errors='coerce')


news_df['sentiment_score'] = news_df['confidence']


sentiment_daily = news_df.groupby('Date')['sentiment_score'].mean().reset_index()
sentiment_daily.rename(columns={'sentiment_score': 'avg_sentiment'}, inplace=True)


df = pd.merge(hist_df, sentiment_daily, on='Date', how='left')
df['avg_sentiment'].fillna(method='ffill', inplace=True)  
df.dropna(inplace=True)  


features = df.drop(columns=['Date', 'Close'])
target = df['Close'].values.reshape(-1, 1)


scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(features)
y_scaled = scaler_y.fit_transform(target)


lookback = 10
X, y = [], []
for i in range(lookback, len(X_scaled)):
    X.append(X_scaled[i-lookback:i])
    y.append(y_scaled[i])
X, y = np.array(X), np.array(y)


split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')


early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=100, batch_size=32,
                    validation_split=0.2, callbacks=[early_stop], verbose=1)


y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_actual = scaler_y.inverse_transform(y_test)


print(f"RMSE: {np.sqrt(mean_squared_error(y_actual, y_pred)):.2f}")
print(f"MAPE: {mean_absolute_percentage_error(y_actual, y_pred):.2%}")
print(f"R² Score: {r2_score(y_actual, y_pred):.2f}")


plt.figure(figsize=(14, 6))
plt.plot(y_actual, label='Actual Close')
plt.plot(y_pred, label='Predicted Close')
plt.title('NIFTY 50 Close Price Prediction (with Sentiment)')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
