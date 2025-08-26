import pandas as pd

# Load the three CSV files
vix_df = pd.read_csv("india_vix_2011_2025.csv")
fii_dii_df = pd.read_csv("fii_dii_data_2011_2024.csv")
historical_df = pd.read_csv("NIFTY50_2011_to_2024.csv")

# Ensure 'Date' column is datetime
vix_df["Date"] = pd.to_datetime(vix_df["Date"])
fii_dii_df["Date"] = pd.to_datetime(fii_dii_df["Date"])
historical_df["Date"] = pd.to_datetime(historical_df["Date"])

# Merge all three files on 'Date'
merged_df = pd.merge(historical_df, fii_dii_df, on="Date", how="outer")
merged_df = pd.merge(merged_df, vix_df, on="Date", how="outer")

# Sort by Date (most recent first)
merged_df = merged_df.sort_values(by="Date", ascending=False).reset_index(drop=True)

# Save merged file
merged_df.to_csv("combined_data.csv", index=False)

print("✅ Combined file created: combined_data.csv (most recent dates first)")
