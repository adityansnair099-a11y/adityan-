import pandas as pd

p = r"c:\Users\DELL\OneDrive\Desktop\sky blue\SkyCity Auckland Restaurants & Bars.csv"
df = pd.read_csv(p)

revenue_cols = ["InStoreRevenue", "UberEatsRevenue", "DoorDashRevenue", "SelfDeliveryRevenue"]
profit_cols = ["InStoreNetProfit", "UberEatsNetProfit", "DoorDashNetProfit", "SelfDeliveryNetProfit"]

for c in revenue_cols + profit_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["total_revenue"] = df[revenue_cols].sum(axis=1)
df["total_profit"] = df[profit_cols].sum(axis=1)
df["profit_margin"] = df["total_profit"] / df["total_revenue"]

print("rows", len(df))
print("avg monthly orders", round(df["MonthlyOrders"].mean(), 2))
print("avg aov", round(df["AOV"].mean(), 2))
print("overall margin", round(df["total_profit"].sum() / df["total_revenue"].sum(), 4))
print("total revenue", round(df["total_revenue"].sum(), 2))
print("total profit", round(df["total_profit"].sum(), 2))
print("negative profit restaurants", int((df["total_profit"] < 0).sum()))
print("top revenue restaurant", df.loc[df["total_revenue"].idxmax(), "RestaurantName"])
print("top profit restaurant", df.loc[df["total_profit"].idxmax(), "RestaurantName"])
print("segment revenue")
print(df.groupby("Segment")["total_revenue"].sum().sort_values(ascending=False).round(2).to_string())
print("segment margin")
print(df.groupby("Segment").apply(lambda g: (g["total_profit"].sum() / g["total_revenue"].sum())).round(4).sort_values(ascending=False).to_string())
print("cuisine revenue")
print(df.groupby("CuisineType")["total_revenue"].sum().sort_values(ascending=False).round(2).to_string())
print("subregion revenue")
print(df.groupby("Subregion")["total_revenue"].sum().sort_values(ascending=False).round(2).to_string())
print("avg channel share")
print(df[["InStoreShare", "UE_share", "DD_share", "SD_share"]].mean().round(4).to_dict())
print("avg delivery cost/order", round(df["DeliveryCostPerOrder"].mean(), 2))
print("avg commission rate", round(df["CommissionRate"].mean(), 4))
print("channel profit totals", {"InStore": df["InStoreNetProfit"].sum(), "UberEats": df["UberEatsNetProfit"].sum(), "DoorDash": df["DoorDashNetProfit"].sum(), "SelfDelivery": df["SelfDeliveryNetProfit"].sum()})
print("top 10 by margin")
print(df.nlargest(10, "profit_margin")[["RestaurantName", "CuisineType", "Segment", "Subregion", "total_revenue", "total_profit", "profit_margin"]].round({"total_revenue":2, "total_profit":2, "profit_margin":4}).to_string(index=False))
print("bottom 10 by margin")
print(df.nsmallest(10, "profit_margin")[["RestaurantName", "CuisineType", "Segment", "Subregion", "total_revenue", "total_profit", "profit_margin"]].round({"total_revenue":2, "total_profit":2, "profit_margin":4}).to_string(index=False))
