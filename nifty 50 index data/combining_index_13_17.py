import os
import pandas as pd

# Path to your folder
folder_path = r"nifty 50 index data"

# Detect all spreadsheet files
files = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls", ".csv"))]

print("Files found:", files)

dfs = []
for file in files:
    file_path = os.path.join(folder_path, file)
    print(f"Reading {file_path}...")
    
    if file.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    dfs.append(df)

if dfs:  # only combine if list not empty
    combined_df = pd.concat(dfs, ignore_index=True)

    # Ensure Date column is in datetime format
    combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
    combined_df = combined_df.dropna(subset=['Date'])  # remove bad rows
    combined_df = combined_df.sort_values('Date')

    # Save to CSV
    output_file = os.path.join(folder_path, "NIFTY50_2013_to_2017_combined.csv")
    combined_df.to_csv(output_file, index=False)
    print(f"✅ Combined CSV saved as: {output_file}")
else:
    print("⚠️ No Excel/CSV files found in folder. Check path or extensions.")
