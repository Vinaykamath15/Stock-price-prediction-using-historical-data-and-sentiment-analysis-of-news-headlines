import pandas as pd

# Load cleaned files
nifty_df = pd.read_csv("nifty50_data_cleaned.csv")
fii_dii_df = pd.read_csv("fii_dii_data_cleaned.csv")
vix_df = pd.read_csv("vix_2017_2025_combined.csv")

# Rename date column in VIX to match others
vix_df.rename(columns={'date': 'Date'}, inplace=True)

# Convert all 'Date' columns to datetime
nifty_df['Date'] = pd.to_datetime(nifty_df['Date'], format='%d-%m-%Y', errors='coerce')
fii_dii_df['Date'] = pd.to_datetime(fii_dii_df['Date'], format='%d-%m-%Y', errors='coerce')
vix_df['Date'] = pd.to_datetime(vix_df['Date'], format='%d-%m-%Y', errors='coerce')

# Drop rows with invalid dates
nifty_df.dropna(subset=['Date'], inplace=True)
fii_dii_df.dropna(subset=['Date'], inplace=True)
vix_df.dropna(subset=['Date'], inplace=True)

# Merge all datasets on Date using outer join to preserve all rows
merged_df = pd.merge(nifty_df, fii_dii_df, on='Date', how='outer')
merged_df = pd.merge(merged_df, vix_df, on='Date', how='outer')

# Sort by Date descending
merged_df.sort_values('Date', ascending=False, inplace=True)

# Optional: Reset index and format date back to string if needed
merged_df.reset_index(drop=True, inplace=True)
merged_df['Date'] = merged_df['Date'].dt.strftime('%d-%m-%Y')

# Save the combined dataset
merged_df.to_csv("combined_nifty_fii_dii_vix.csv", index=False)

print("✅ All data combined and saved as 'combined_nifty_fii_dii_vix.csv'.")
