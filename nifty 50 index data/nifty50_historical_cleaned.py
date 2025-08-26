import pandas as pd

# Load the file
df = pd.read_csv("NIFTY 50_Historical_PR_01012017to01012025.csv")

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Drop fully empty rows
df.dropna(how='all', inplace=True)

# Try parsing the date flexibly
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows where the date couldn’t be parsed
df.dropna(subset=['Date'], inplace=True)

# Format date to 'dd-mm-yyyy'
df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

# Save cleaned version
df.to_csv("nifty50_data_cleaned.csv", index=False)
