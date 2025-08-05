import yfinance as yf
import pandas as pd

# Define the ticker symbol for India VIX
ticker = "^INDIAVIX"

# Define start and end dates for 2021
start_date = "2021-01-01"
end_date = "2022-01-01"

# Download historical data from Yahoo Finance
vix_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")

# Reset the index to move 'Date' from index to column
vix_data.reset_index(inplace=True)

# Optional: Display the first few rows
print(vix_data.head())

# Save full data to CSV
vix_data.to_csv("vix_2021_full.csv", index=False)

print("✅ India VIX data for 2021 downloaded and saved as 'vix_2021_full.csv'")
