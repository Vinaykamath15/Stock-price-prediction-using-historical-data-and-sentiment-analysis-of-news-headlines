import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping

# --- Load Historical Data --- #
hist_df = pd.read_csv('/kaggle/input/combined-stock-data/combined_nifty_fii_dii_vix.csv')
hist_df['Date'] = pd.to_datetime(hist_df['Date'], format='%d-%m-%Y')
hist_df.drop(columns=['Index Name'], errors='ignore', inplace=True)
hist_df.sort_values('Date', inplace=True)

# --- Load News Sentiment Data --- #
news_df = pd.read_csv('/kaggle/input/financial-news/financial_news.csv')
news_df['Date'] = pd.to_datetime(news_df['Date'], format='%d/%m/%y')
news_df['confidence'] = pd.to_numeric(news_df['confidence'], errors='coerce')

# Convert sentiment to numeric (optional – you already have compound/confidence if using VADER)
news_df['sentiment_score'] = news_df['confidence']

# --- Aggregate sentiment scores by date --- #
sentiment_daily = news_df.groupby('Date')['sentiment_score'].mean().reset_index()
sentiment_daily.rename(columns={'sentiment_score': 'avg_sentiment'}, inplace=True)

# --- Merge with historical data --- #
df = pd.merge(hist_df, sentiment_daily, on='Date', how='left')
df['avg_sentiment'].fillna(method='ffill', inplace=True)  # Forward fill
df.dropna(inplace=True)  # Drop any remaining NaNs (should be safe now)

# --- Features & Target --- #
features = df.drop(columns=['Date', 'Close'])
target = df['Close'].values.reshape(-1, 1)

# --- Scale Features & Target --- #
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(features)
y_scaled = scaler_y.fit_transform(target)

# --- Sequence Generation --- #
lookback = 10
X, y = [], []
for i in range(lookback, len(X_scaled)):
    X.append(X_scaled[i-lookback:i])
    y.append(y_scaled[i])
X, y = np.array(X), np.array(y)

# --- Train/Test Split --- #
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# --- Model --- #
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# --- Training --- #
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=100, batch_size=32,
                    validation_split=0.2, callbacks=[early_stop], verbose=1)

# --- Prediction --- #
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_actual = scaler_y.inverse_transform(y_test)

# --- Metrics --- #
print(f"RMSE: {np.sqrt(mean_squared_error(y_actual, y_pred)):.2f}")
print(f"MAPE: {mean_absolute_percentage_error(y_actual, y_pred):.2%}")
print(f"R² Score: {r2_score(y_actual, y_pred):.2f}")

# --- Plot --- #
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
