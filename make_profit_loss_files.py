import pandas as pd
from pathlib import Path

base = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue")
source = base / "SkyCity Auckland Restaurants & Bars.csv"

if not source.exists():
    raise FileNotFoundError(f"Source file not found: {source}")

df = pd.read_csv(source)
revenue_cols = [c for c in df.columns if 'Revenue' in c]
profit_cols = [c for c in df.columns if 'NetProfit' in c]
for c in revenue_cols + profit_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

df['total_revenue'] = df[revenue_cols].sum(axis=1)
df['total_profit'] = df[profit_cols].sum(axis=1)

profit = df[df['total_profit'] >= 0].copy()
loss = df[df['total_profit'] < 0].copy()

profit.to_csv(base / 'SkyCity Restaurants Profit.csv', index=False)
loss.to_csv(base / 'SkyCity Restaurants Loss.csv', index=False)

print(f'profit_rows={len(profit)}')
print(f'loss_rows={len(loss)}')
print(f'profit_file={base / "SkyCity Restaurants Profit.csv"}')
print(f'loss_file={base / "SkyCity Restaurants Loss.csv"}')
