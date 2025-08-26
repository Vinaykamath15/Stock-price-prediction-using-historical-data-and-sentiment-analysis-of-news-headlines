import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping

# Load data
df = pd.read_csv('/kaggle/input/combined-stock-data/combined_nifty_fii_dii_vix.csv')

# Clean and prep
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df.sort_values('Date', inplace=True)
df.drop(columns=['Index Name'], errors='ignore', inplace=True)

# Select features (everything except Close and Date) and target (Close)
features = df.drop(columns=['Date', 'Close'])
target = df['Close'].values.reshape(-1, 1)

# Scale features and target
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(features)
y_scaled = scaler_y.fit_transform(target)

# Create sequences for LSTM
lookback = 10
X, y = [], []
for i in range(lookback, len(X_scaled)):
    X.append(X_scaled[i-lookback:i])
    y.append(y_scaled[i])
X, y = np.array(X), np.array(y)

# Split train/test
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Build model
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# Train
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=100, batch_size=32,
                    validation_split=0.2, callbacks=[early_stop], verbose=1)

# Predict
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_actual = scaler_y.inverse_transform(y_test)

# Metrics
rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
mape = mean_absolute_percentage_error(y_actual, y_pred)
r2 = r2_score(y_actual, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2%}")
print(f"R² Score: {r2:.2f}")

# Plot
plt.figure(figsize=(14, 6))
plt.plot(y_actual, label='Actual Close')
plt.plot(y_pred, label='Predicted Close')
plt.title('NIFTY 50 Close Price Prediction')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
