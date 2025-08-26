import os
import pandas as pd

# Paths to your two cleaned CSVs
file1 = r"D:\stock-price-prediction\nifty 50 index data\NIFTY50_2011-04_to_2013-01.csv"
file2 = r"D:\stock-price-prediction\nifty 50 index data\NIFTY50_2013_to_2017_combined.csv"

# Read both
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Combine them
combined_df = pd.concat([df1, df2], ignore_index=True)

# Ensure date is datetime and sort
combined_df["Date"] = pd.to_datetime(combined_df["Date"], errors="coerce")
combined_df = combined_df.dropna(subset=["Date"])
combined_df = combined_df.sort_values("Date")

# Save combined file
output_file = r"D:\stock-price-prediction\nifty 50 index data\NIFTY50_2011_to_2017.csv"
combined_df.to_csv(output_file, index=False)

print(f"✅ Combined file saved as: {output_file}")
