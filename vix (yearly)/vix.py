import pandas as pd

# File paths
combined_file = r"D:\stock-price-prediction\vix (yearly)\vix_2017_2025_combined.csv"
old_file = r"D:\stock-price-prediction\vix (yearly)\vix_2011_to_2017.csv"

# Load the existing combined file (2017–2025)
df_new = pd.read_csv(combined_file)
df_new.columns = [col.strip().lower() for col in df_new.columns]

# Ensure it only has the expected columns
if 'close' in df_new.columns:
    df_new = df_new[['date', 'close']].rename(columns={'close': 'vix'})
elif 'vix' in df_new.columns:
    df_new = df_new[['date', 'vix']]

# Load the older file (2011–2017)
df_old = pd.read_csv(old_file)
df_old.columns = [col.strip().lower() for col in df_old.columns]

# Standardize structure
if 'close' in df_old.columns:
    df_old = df_old[['date', 'close']].rename(columns={'close': 'vix'})
elif 'closing value' in df_old.columns:
    df_old = df_old[['date', 'closing value']].rename(columns={'closing value': 'vix'})
elif 'vix' in df_old.columns:
    df_old = df_old[['date', 'vix']]

# Convert and clean values
df_new['date'] = pd.to_datetime(df_new['date'], errors='coerce')
df_old['date'] = pd.to_datetime(df_old['date'], errors='coerce')

df_new['vix'] = pd.to_numeric(df_new['vix'], errors='coerce')
df_old['vix'] = pd.to_numeric(df_old['vix'], errors='coerce')

df_new = df_new.dropna(subset=['date', 'vix'])
df_old = df_old.dropna(subset=['date', 'vix'])

# Combine both datasets
final_df = pd.concat([df_new, df_old], ignore_index=True)

# 🔥 Sort with most recent first
final_df = final_df.sort_values(by='date', ascending=False).reset_index(drop=True)

# Format dates to dd-mm-yyyy AFTER sorting
final_df['date'] = final_df['date'].dt.strftime('%d-%m-%Y')

# Save result
output_file = r"D:\stock-price-prediction\vix (yearly)\vix_2011_2025_combined.csv"
final_df.to_csv(output_file, index=False)

print(f"✅ VIX data successfully combined and saved as: {output_file}")
print(f"   Total rows in final dataset: {len(final_df)}")
