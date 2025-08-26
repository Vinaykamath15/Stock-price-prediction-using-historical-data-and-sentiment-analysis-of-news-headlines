import pandas as pd
from pathlib import Path

# --- paths (edit if yours differ)
file_1117 = Path(r"D:\stock-price-prediction\nifty 50 index data\NIFTY50_2011_to_2017.csv")
file_1724 = Path(r"D:\stock-price-prediction\nifty 50 index data\nifty50_data_cleaned.csv")
out_file   = Path(r"D:\stock-price-prediction\nifty 50 index data\NIFTY50_2011_to_2024.csv")

def read_clean(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # strip column whitespace and standardize names
    df.columns = df.columns.str.strip()
    rename = {c: c.strip() for c in df.columns}  # just to be safe
    df = df.rename(columns=rename)

    # Ensure Date exists
    if "Date" not in df.columns:
        raise ValueError(f"'Date' column not found in {path}")

    # Add Index Name if missing
    if "Index Name" not in df.columns:
        df.insert(0, "Index Name", "NIFTY 50")
    else:
        # normalize the values just in case
        df["Index Name"] = "NIFTY 50"

    # Keep only the expected columns (others are ignored)
    keep = ["Index Name", "Date", "Open", "High", "Low", "Close"]
    df = df[[c for c in keep if c in df.columns]]

    # Robust date parsing: try multiple patterns
    s = df["Date"].astype(str).str.strip().str.replace(r"[./]", "-", regex=True)
    dt = pd.to_datetime(s, errors="coerce", dayfirst=True)              # handles 01-12-2016, 01-Jan-13
    mask = dt.isna()
    if mask.any():
        dt2 = pd.to_datetime(s[mask], format="%Y-%m-%d", errors="coerce") # handles 2011-04-01
        dt.loc[mask] = dt2
    mask = dt.isna()
    if mask.any():
        dt2 = pd.to_datetime(s[mask], format="%d-%b-%y", errors="coerce") # handles 01-Jan-13
        dt.loc[mask] = dt2

    df["Date"] = dt
    bad = df["Date"].isna().sum()
    if bad:
        print(f"⚠️  {bad} rows in {path.name} had unparseable dates and will be dropped.")
        df = df.dropna(subset=["Date"])

    # Ensure numeric OHLC (strings with commas become numbers)
    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace(" ", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# Read both files
df_1117 = read_clean(file_1117)
df_1724 = read_clean(file_1724)

# Quick diagnostics before combining
def info(tag, df):
    if not df.empty:
        print(f"{tag}: {len(df)} rows | {df['Date'].min().date()} → {df['Date'].max().date()}")
    else:
        print(f"{tag}: 0 rows")

info("2011–2017", df_1117)
info("2017–2024", df_1724)

# Combine, de-dup by Date (keep the newer file’s values if overlap)
combined = pd.concat([df_1724, df_1117], ignore_index=True)
combined = combined.sort_values("Date", ascending=False)
combined = combined.drop_duplicates(subset=["Date"], keep="first")

# Final diagnostics
info("COMBINED", combined)
print(combined.head(3))
print(combined.tail(3))

# Save
combined.to_csv(out_file, index=False)
print(f"✅ Saved: {out_file}")
