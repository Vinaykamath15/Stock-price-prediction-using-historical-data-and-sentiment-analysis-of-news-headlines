import yfinance as yf
import pandas as pd

# Define ticker and date range
ticker = "^NSEI"   # NIFTY 50 Index
start_date = "2011-04-01"
end_date = "2013-01-01"

# Download data
data = yf.download(ticker, start=start_date, end=end_date)

# Reset index so Date is a column
data.reset_index(inplace=True)

# Rename columns to match your existing dataset
data = data.rename(columns={
    "Date": "Date",
    "Open": "Open",
    "High": "High",
    "Low": "Low",
    "Close": "Close",
    "Volume": "Shares Traded"
})

# Add placeholder for Turnover (₹ Cr), since Yahoo doesn't provide it
data["Turnover (₹ Cr)"] = None

# Reorder columns to match your files
data = data[["Date", "Open", "High", "Low", "Close", "Shares Traded", "Turnover (₹ Cr)"]]

# Save as CSV
output_file = r"D:\stock-price-prediction\nifty 50 index data\NIFTY50_2011-04_to_2013-01.csv"
data.to_csv(output_file, index=False)

print(f"✅ Data saved to {output_file}")
