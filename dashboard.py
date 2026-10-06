from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="SkyCity | Portfolio Analytics",
    page_icon="S",
    layout="wide",
)

DATA_PATH = Path(__file__).with_name("SkyCity Auckland Restaurants & Bars.csv")
CHANNELS = {
    "In-store": ("InStoreRevenue", "InStoreNetProfit", "InStoreShare"),
    "Uber Eats": ("UberEatsRevenue", "UberEatsNetProfit", "UE_share"),
    "DoorDash": ("DoorDashRevenue", "DoorDashNetProfit", "DD_share"),
    "Self-delivery": ("SelfDeliveryRevenue", "SelfDeliveryNetProfit", "SD_share"),
}
COLORS = ["#155b58", "#d18a30", "#427eaa", "#bd5b4c"]

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dfe7e5;
        border-left: 4px solid #155b58;
        padding: 14px 16px;
        border-radius: 4px;
    }
    [data-testid="stMetricLabel"] p {color: #56646b; font-size: 0.82rem;}
    [data-testid="stMetricValue"] {color: #18363a; font-size: 1.65rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=60)
def load_data(file_path, modified_time):
    del modified_time
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    data = pd.read_csv(file_path)
    numeric_columns = [column for values in CHANNELS.values() for column in values]
    numeric_columns += ["AOV", "MonthlyOrders", "DeliveryCostPerOrder", "CommissionRate"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data["TotalRevenue"] = data[[values[0] for values in CHANNELS.values()]].sum(axis=1)
    data["TotalProfit"] = data[[values[1] for values in CHANNELS.values()]].sum(axis=1)
    data["ProfitMargin"] = data["TotalProfit"].div(data["TotalRevenue"].where(data["TotalRevenue"] != 0))
    return data


try:
    source_modified = DATA_PATH.stat().st_mtime
    df = load_data(str(DATA_PATH), source_modified)
except FileNotFoundError as error:
    st.error(f"{error}. Place the source CSV beside dashboard.py and refresh the page.")
    st.stop()

st.title("SkyCity Auckland | Restaurant Portfolio")
st.caption("Interactive analytics from the local source CSV. Refresh checks for file updates; no external live feed is connected.")

with st.sidebar:
    st.header("Portfolio filters")
    if st.button("Refresh source data", width="stretch"):
        load_data.clear()
        st.rerun()

    segment_options = sorted(df["Segment"].dropna().unique())
    selected_segments = st.multiselect("Format", segment_options, default=segment_options)
    segment_data = df[df["Segment"].isin(selected_segments)]

    region_options = sorted(segment_data["Subregion"].dropna().unique())
    selected_regions = st.multiselect("Subregion", region_options, default=region_options)
    region_data = segment_data[segment_data["Subregion"].isin(selected_regions)]

    cuisine_options = sorted(region_data["CuisineType"].dropna().unique())
    selected_cuisines = st.multiselect("Cuisine", cuisine_options, default=cuisine_options)

    profit_status = st.radio("Profit status", ["All", "Profitable", "Loss-making"], horizontal=True)
    st.divider()
    st.caption(f"Source file modified: {pd.Timestamp(source_modified, unit='s').strftime('%d %b %Y, %H:%M')}")
    st.caption("Amounts use the source file's currency, which is unspecified.")

filtered = df[
    df["Segment"].isin(selected_segments)
    & df["Subregion"].isin(selected_regions)
    & df["CuisineType"].isin(selected_cuisines)
]
if profit_status == "Profitable":
    filtered = filtered[filtered["TotalProfit"] >= 0]
elif profit_status == "Loss-making":
    filtered = filtered[filtered["TotalProfit"] < 0]

if filtered.empty:
    st.info("No restaurants match these filters. Adjust the selections in the sidebar.")
    st.stop()

revenue_total = filtered["TotalRevenue"].sum()
profit_total = filtered["TotalProfit"].sum()
margin = profit_total / revenue_total if revenue_total else 0
loss_count = int((filtered["TotalProfit"] < 0).sum())

metric_columns = st.columns(4)
metric_columns[0].metric("Restaurants", f"{len(filtered):,}")
metric_columns[1].metric("Revenue", f"${revenue_total / 1_000_000:.2f}m")
metric_columns[2].metric("Net profit", f"${profit_total / 1_000_000:.2f}m")
metric_columns[3].metric("Profit margin", f"{margin:.1%}")
st.info(f"{loss_count:,} selected restaurants ({loss_count / len(filtered):.1%}) are loss-making.")

st.divider()
left, right = st.columns([1.15, 0.85])
with left:
    st.subheader("Revenue by operating format")
    segment_summary = (
        filtered.groupby("Segment", as_index=False)
        .agg(Revenue=("TotalRevenue", "sum"), Profit=("TotalProfit", "sum"))
        .sort_values("Revenue", ascending=True)
    )
    figure = px.bar(
        segment_summary,
        x="Revenue",
        y="Segment",
        color="Segment",
        hover_data={"Profit": ":$,.0f", "Revenue": ":$,.0f"},
        color_discrete_sequence=COLORS,
    )
    figure.update_layout(showlegend=False, template="plotly_white", xaxis_title="Revenue", yaxis_title="")
    st.plotly_chart(figure, width="stretch")

with right:
    st.subheader("Channel revenue mix")
    channel_summary = pd.DataFrame([
        {"Channel": name, "Revenue": filtered[values[0]].sum(), "Profit": filtered[values[1]].sum()}
        for name, values in CHANNELS.items()
    ])
    figure = px.pie(
        channel_summary,
        names="Channel",
        values="Revenue",
        hole=0.58,
        color="Channel",
        color_discrete_sequence=COLORS,
    )
    figure.update_traces(textposition="inside", textinfo="percent")
    figure.update_layout(template="plotly_white", legend_title_text="")
    st.plotly_chart(figure, width="stretch")

left, right = st.columns(2)
with left:
    st.subheader("Profit margin by format")
    segment_margin = (
        filtered.groupby("Segment", as_index=False)
        .agg(Revenue=("TotalRevenue", "sum"), Profit=("TotalProfit", "sum"))
    )
    segment_margin["Margin"] = segment_margin["Profit"].div(segment_margin["Revenue"].where(segment_margin["Revenue"] != 0))
    segment_margin = segment_margin.sort_values("Margin")
    figure = px.bar(
        segment_margin,
        x="Margin",
        y="Segment",
        color="Margin",
        color_continuous_scale=["#bd5b4c", "#d9a441", "#155b58"],
        hover_data={"Profit": ":$,.0f", "Margin": ":.1%"},
    )
    figure.update_layout(template="plotly_white", coloraxis_showscale=False, xaxis_tickformat=".0%", xaxis_title="Margin", yaxis_title="")
    st.plotly_chart(figure, width="stretch")

with right:
    st.subheader("Revenue and margin by subregion")
    region_summary = (
        filtered.groupby("Subregion", as_index=False)
        .agg(Revenue=("TotalRevenue", "sum"), Profit=("TotalProfit", "sum"))
    )
    region_summary["Margin"] = region_summary["Profit"].div(region_summary["Revenue"].where(region_summary["Revenue"] != 0))
    figure = px.scatter(
        region_summary,
        x="Revenue",
        y="Margin",
        size="Revenue",
        color="Subregion",
        hover_name="Subregion",
        hover_data={"Profit": ":$,.0f", "Margin": ":.1%"},
        color_discrete_sequence=COLORS,
    )
    figure.update_layout(template="plotly_white", xaxis_title="Revenue", yaxis_tickformat=".0%", yaxis_title="Profit margin")
    st.plotly_chart(figure, width="stretch")

st.subheader("Restaurant performance")
table = filtered[["RestaurantName", "CuisineType", "Segment", "Subregion", "MonthlyOrders", "TotalRevenue", "TotalProfit", "ProfitMargin"]].copy()
table = table.sort_values("TotalProfit", ascending=False)
st.dataframe(
    table,
    width="stretch",
    hide_index=True,
    column_config={
        "RestaurantName": "Restaurant",
        "CuisineType": "Cuisine",
        "Segment": "Format",
        "Subregion": "Subregion",
        "MonthlyOrders": st.column_config.NumberColumn("Monthly orders", format="%d"),
        "TotalRevenue": st.column_config.NumberColumn("Revenue", format="$%.2f"),
        "TotalProfit": st.column_config.NumberColumn("Net profit", format="$%.2f"),
        "ProfitMargin": st.column_config.NumberColumn("Margin", format="%.1f%%"),
    },
)
st.caption("Figures are calculated from the supplied channel revenue and net-profit fields. Source currency and reporting period are not identified.")
