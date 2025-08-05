from nsepy import get_fii_dii
from datetime import date
df = get_fii_dii(date(2017, 1, 1), date(2025, 1, 1))
df.to_csv("fii_dii_data.csv", index=False)
