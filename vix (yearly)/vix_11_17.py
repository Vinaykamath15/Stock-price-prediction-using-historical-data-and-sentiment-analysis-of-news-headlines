import yfinance as yf
import pandas as pd

# Define the ticker symbol for India VIX
ticker = "^INDIAVIX"

# Define start and end dates (April 2011 to Jan 1, 2017)
start_date = "2011-04-01"
end_date = "2017-01-01"

# Download historical data from Yahoo Finance
vix_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")

# Reset the index to move 'Date' from index to column
vix_data.reset_index(inplace=True)

# Save full data to CSV
vix_data.to_csv("vix_2011_to_2017.csv", index=False)

print("✅ India VIX data from Apr 2011 to Jan 2017 downloaded and saved as 'vix_2011_to_2017.csv'")
print(vix_data.head())
print(vix_data.tail())
