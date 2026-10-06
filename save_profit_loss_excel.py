import pandas as pd
from pathlib import Path

base = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue")
for name in ["SkyCity Restaurants Profit.csv", "SkyCity Restaurants Loss.csv"]:
    csv_path = base / name
    if not csv_path.exists():
        print(f"Missing: {csv_path}")
        continue
    df = pd.read_csv(csv_path)
    xlsx_path = csv_path.with_suffix(".xlsx")
    df.to_excel(xlsx_path, index=False)
    print(f"Saved: {xlsx_path}")
