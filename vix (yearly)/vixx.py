import yfinance as yf
import pandas as pd

# Download India VIX (Yahoo symbol: ^INDIAVIX)
ticker = "^INDIAVIX"

# Fetch data
data = yf.download(ticker, start="2011-04-01", end="2025-01-01")

# Keep only Date and Close
df = data[["Close"]].reset_index()

# Rename columns
df.rename(columns={"Date": "date", "Close": "vix"}, inplace=True)

# Sort most recent first
df = df.sort_values("date", ascending=False).reset_index(drop=True)

# Save to CSV
output_path = "india_vix_2011_2025.csv"
df.to_csv(output_path, index=False)

print("✅ Saved:", output_path)
