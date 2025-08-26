import pandas as pd

# File paths
file_new = r"fii_dii_data_cleaned.csv"     # 2017–2025
file_old = r"fii_dii_data_cleaned2.csv"    # older (≤2017)

# Load both datasets
df_new = pd.read_csv(file_new)
df_old = pd.read_csv(file_old)

# Standardize column names (strip spaces, lowercase, replace multiple underscores)
df_new.columns = [col.strip().replace(" ", "_").replace("__", "_") for col in df_new.columns]
df_old.columns = [col.strip().replace(" ", "_").replace("__", "_") for col in df_old.columns]

# Convert Date to datetime
df_new['Date'] = pd.to_datetime(df_new['Date'], errors='coerce', dayfirst=True)
df_old['Date'] = pd.to_datetime(df_old['Date'], errors='coerce', dayfirst=True)

# Drop rows where Date is invalid
df_new = df_new.dropna(subset=['Date'])
df_old = df_old.dropna(subset=['Date'])

# Combine
final_df = pd.concat([df_new, df_old], ignore_index=True)

# Sort by date (most recent first)
final_df = final_df.sort_values(by='Date', ascending=False).reset_index(drop=True)

# Save combined file
output_file = r"D:\stock-price-prediction\datasets (pre cleaning)\fii_dii_data_2011_2025.csv"
final_df.to_csv(output_file, index=False)

print(f"✅ Combined FII/DII data saved as: {output_file}")
print(f"   Total rows in final dataset: {len(final_df)}")
