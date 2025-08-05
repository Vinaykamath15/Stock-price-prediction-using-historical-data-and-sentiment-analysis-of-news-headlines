import pandas as pd
import os
import glob

# Folder where all the VIX CSV files (NSE + Yahoo) are stored
folder_path = 'vix'  # change this to your actual folder name if different
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

df_list = []

for file in all_files:
    df = pd.read_csv(file)
    df.columns = [col.strip().lower() for col in df.columns]

    # Normalize date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
    else:
        continue  # Skip if no Date column

    # Extract correct close value — check which column exists
    if 'close' in df.columns:
        df = df[['date', 'close']]
        df.rename(columns={'close': 'vix'}, inplace=True)
    elif 'closing value' in df.columns:
        df = df[['date', 'closing value']]
        df.rename(columns={'closing value': 'vix'}, inplace=True)
    else:
        continue  # Skip files without recognizable close column

    # Clean
    df['vix'] = pd.to_numeric(df['vix'], errors='coerce')
    df = df.dropna(subset=['vix'])

    df_list.append(df)

# Combine everything
vix_combined = pd.concat(df_list, ignore_index=True)

# Remove duplicates if any
vix_combined.drop_duplicates(subset='date', keep='first', inplace=True)

# Sort descending (most recent first)
vix_combined.sort_values(by='date', ascending=False, inplace=True)

# Format date if needed
vix_combined['date'] = vix_combined['date'].dt.strftime('%d-%m-%Y')

# Save the final combined file
vix_combined.to_csv("vix_2017_2025_combined.csv", index=False)

print("✅ Combined VIX file saved as 'vix_2017_2025_combined.csv'. Rows:", len(vix_combined))
