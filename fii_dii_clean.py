import pandas as pd

# Load the data
df = pd.read_csv("fii_dii_data.csv")

# Manually assign correct column names
df.columns = [
    'Date',
    'FII_Gross_Purchase',
    'FII_Gross_Sales',
    'FII_Net_Purchase_Sales',
    'DII_Gross_Purchase',
    'DII_Gross_Sales',
    'DII_Net_Purchase_Sales'
]

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')

# Drop rows with invalid/missing dates
df.dropna(subset=['Date'], inplace=True)

# Remove commas and convert all numeric columns to float
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows that are completely empty (just in case)
df.dropna(how='all', inplace=True)

# Format 'Date' to 'dd-mm-yyyy'
df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

# Save cleaned file
df.to_csv("fii_dii_data_cleaned.csv", index=False)
