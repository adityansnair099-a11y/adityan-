import csv
import json
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).parent
SOURCE = BASE / "SkyCity Auckland Restaurants & Bars.csv"
OUTPUT = BASE / "SkyCity_Auckland_Portfolio_Analytics.html"

REVENUE_COLUMNS = {
    "In-store": "InStoreRevenue",
    "Uber Eats": "UberEatsRevenue",
    "DoorDash": "DoorDashRevenue",
    "Self-delivery": "SelfDeliveryRevenue",
}
PROFIT_COLUMNS = {
    "InStoreNetProfit",
    "UberEatsNetProfit",
    "DoorDashNetProfit",
    "SelfDeliveryNetProfit",
}

with SOURCE.open("r", encoding="utf-8-sig", newline="") as source_file:
    source_rows = list(csv.DictReader(source_file))

records = []
for row in source_rows:
    record = {
        "RestaurantName": row["RestaurantName"],
        "CuisineType": row["CuisineType"],
        "Segment": row["Segment"],
        "Subregion": row["Subregion"],
        "MonthlyOrders": int(float(row["MonthlyOrders"] or 0)),
    }
    for column in REVENUE_COLUMNS.values():
        record[column] = float(row[column] or 0)
    for column in PROFIT_COLUMNS:
        record[column] = float(row[column] or 0)
    record["TotalRevenue"] = sum(record[column] for column in REVENUE_COLUMNS.values())
    record["TotalProfit"] = sum(record[column] for column in PROFIT_COLUMNS)
    record["ProfitMargin"] = record["TotalProfit"] / record["TotalRevenue"] if record["TotalRevenue"] else 0
    records.append(record)

payload = json.dumps(
    {"records": records, "generated": datetime.now().strftime("%d %b %Y, %H:%M")},
    ensure_ascii=True,
    separators=(",", ":"),
).replace("</", "<\\/")

html_template = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#163d45">
  <title>SkyCity | Portfolio Analytics</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #203238;
      --muted: #66777a;
      --line: #dce5e2;
      --paper: #f4f7f5;
      --white: #fff;
      --pine: #155b58;
      --pine-deep: #163d45;
      --ochre: #c7832f;
      --blue: #427eaa;
      --coral: #bd5b4c;
      --mint: #e9f2ef;
      --shadow: 0 5px 18px rgba(28, 56, 57, .06);
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--paper); color: var(--ink); font-family: "Aptos", "Segoe UI", sans-serif; }
    .shell { max-width: 1440px; margin: 0 auto; padding: 30px 36px 52px; }
    .masthead { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; border-bottom: 1px solid var(--line); padding-bottom: 20px; }
    .eyebrow { color: var(--pine); text-transform: uppercase; font-size: 11px; font-weight: 700; letter-spacing: .12em; }
    h1 { margin: 8px 0 0; font-family: Georgia, "Times New Roman", serif; font-size: 34px; font-weight: 500; letter-spacing: 0; }
    .subhead { color: var(--muted); margin: 7px 0 0; font-size: 14px; }
    .source-stamp { color: var(--muted); text-align: right; font-size: 12px; line-height: 1.65; white-space: nowrap; }
    .filters { display: grid; grid-template-columns: repeat(4, minmax(140px, 1fr)) auto; gap: 12px; align-items: end; padding: 20px 0; }
    .filter label { display: block; margin-bottom: 6px; color: var(--muted); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; }
    select, input[type="search"] { width: 100%; min-height: 42px; border: 1px solid #c9d6d2; border-radius: 4px; padding: 0 11px; background: var(--white); color: var(--ink); font: inherit; font-size: 14px; }
    button { min-height: 42px; border: 1px solid var(--pine); border-radius: 4px; padding: 0 15px; background: var(--pine); color: var(--white); font: inherit; font-size: 13px; font-weight: 650; cursor: pointer; }
    button:hover { background: var(--pine-deep); }
    button:focus-visible, select:focus-visible, input:focus-visible { outline: 3px solid rgba(66, 126, 170, .3); outline-offset: 2px; }
    .kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
    .kpi { min-height: 104px; padding: 17px 18px; border: 1px solid var(--line); border-top: 3px solid var(--pine); border-radius: 4px; background: var(--white); box-shadow: var(--shadow); }
    .kpi:nth-child(2) { border-top-color: var(--blue); }
    .kpi:nth-child(3) { border-top-color: var(--ochre); }
    .kpi:nth-child(4) { border-top-color: var(--coral); }
    .kpi-label { color: var(--muted); font-size: 12px; }
    .kpi-value { margin-top: 8px; font-family: Georgia, "Times New Roman", serif; font-size: 27px; line-height: 1; }
    .loss-note { margin: 13px 0 21px; padding: 11px 14px; border-left: 3px solid var(--coral); background: #fbefec; color: #65372f; font-size: 13px; }
    .charts { display: grid; grid-template-columns: 1.1fr .9fr; gap: 14px; }
    .panel { min-width: 0; border: 1px solid var(--line); border-radius: 4px; background: var(--white); box-shadow: var(--shadow); padding: 19px 20px; }
    .panel h2 { margin: 0; font-family: Georgia, "Times New Roman", serif; font-size: 19px; font-weight: 500; }
    .panel-note { margin: 5px 0 16px; color: var(--muted); font-size: 12px; }
    .bar-row { display: grid; grid-template-columns: minmax(105px, 1.05fr) 2.5fr minmax(74px, .65fr); gap: 10px; align-items: center; margin: 12px 0; font-size: 12px; }
    .bar-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .track { height: 10px; overflow: hidden; border-radius: 2px; background: #edf2f0; }
    .fill { height: 100%; min-width: 2px; border-radius: 2px; background: var(--pine); }
    .bar-value { text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); }
    .donut-layout { display: flex; align-items: center; justify-content: center; gap: 24px; min-height: 205px; }
    .donut { width: 164px; height: 164px; flex: 0 0 164px; border-radius: 50%; position: relative; }
    .donut::after { content: ""; position: absolute; inset: 28px; border: 1px solid var(--line); border-radius: 50%; background: white; }
    .legend { display: grid; gap: 12px; }
    .legend-item { display: grid; grid-template-columns: 10px minmax(76px, auto) auto; gap: 8px; align-items: center; font-size: 12px; }
    .swatch { width: 9px; height: 9px; border-radius: 50%; }
    .legend-value { color: var(--muted); font-variant-numeric: tabular-nums; }
    .dual { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
    .margin-row { margin: 15px 0; }
    .margin-caption { display: flex; justify-content: space-between; gap: 8px; margin-bottom: 7px; font-size: 12px; }
    .margin-number { font-weight: 700; font-variant-numeric: tabular-nums; }
    .margin-track { position: relative; height: 10px; border-radius: 2px; background: linear-gradient(to right, transparent 49.5%, #98aaa5 49.5% 50.5%, transparent 50.5%); }
    .margin-fill { position: absolute; top: 1px; height: 8px; border-radius: 2px; }
    .region-row { margin: 13px 0; }
    .region-heading { display: flex; justify-content: space-between; gap: 8px; margin-bottom: 6px; font-size: 12px; }
    .table-section { margin-top: 14px; }
    .table-tools { display: grid; grid-template-columns: 1fr auto auto; gap: 10px; align-items: center; margin: 14px 0 10px; }
    .table-count { color: var(--muted); font-size: 12px; white-space: nowrap; }
    .table-wrap { overflow: auto; max-height: 540px; border: 1px solid var(--line); }
    table { width: 100%; border-collapse: collapse; background: var(--white); font-size: 12px; }
    th, td { padding: 10px 12px; border-bottom: 1px solid #edf1ef; text-align: left; white-space: nowrap; }
    th { position: sticky; top: 0; z-index: 1; background: #edf3f0; color: #42565a; font-size: 10px; text-transform: uppercase; letter-spacing: .06em; }
    td.numeric { text-align: right; font-variant-numeric: tabular-nums; }
    .positive { color: var(--pine); }
    .negative { color: var(--coral); }
    .empty { padding: 22px; color: var(--muted); text-align: center; }
    footer { margin-top: 18px; color: var(--muted); font-size: 11px; line-height: 1.6; }
    @media (max-width: 900px) {
      .shell { padding: 22px 18px 38px; }
      .masthead { align-items: flex-start; flex-direction: column; }
      .source-stamp { text-align: left; white-space: normal; }
      .filters { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .filters button { grid-column: 1 / -1; }
      .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .charts, .dual { grid-template-columns: 1fr; }
    }
    @media (max-width: 520px) {
      h1 { font-size: 28px; }
      .filters { grid-template-columns: 1fr 1fr; gap: 9px; }
      .kpi { min-height: 90px; padding: 13px; }
      .kpi-value { font-size: 23px; }
      .panel { padding: 16px 13px; }
      .donut-layout { gap: 12px; }
      .donut { width: 132px; height: 132px; flex-basis: 132px; }
      .donut::after { inset: 24px; }
      .bar-row { grid-template-columns: minmax(80px, 1fr) 1.4fr 70px; gap: 7px; }
      .table-tools { grid-template-columns: 1fr auto; }
      .table-count { grid-column: 1 / -1; grid-row: 2; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <header class="masthead">
      <div>
        <div class="eyebrow">SkyCity Auckland · Portfolio intelligence</div>
        <h1>Restaurant performance</h1>
        <p class="subhead">Revenue, profitability and channel mix across the restaurant portfolio</p>
      </div>
      <div class="source-stamp">Embedded source snapshot<br><span id="generated"></span><br>Currency and reporting period not specified</div>
    </header>

    <section class="filters" aria-label="Dashboard filters">
      <div class="filter"><label for="formatFilter">Format</label><select id="formatFilter"><option value="">All formats</option></select></div>
      <div class="filter"><label for="regionFilter">Subregion</label><select id="regionFilter"><option value="">All subregions</option></select></div>
      <div class="filter"><label for="cuisineFilter">Cuisine</label><select id="cuisineFilter"><option value="">All cuisines</option></select></div>
      <div class="filter"><label for="profitFilter">Profit status</label><select id="profitFilter"><option value="all">All results</option><option value="profit">Non-loss-making</option><option value="loss">Loss-making</option></select></div>
      <button id="resetButton" type="button">Reset filters</button>
    </section>

    <section class="kpis" aria-label="Key figures">
      <div class="kpi"><div class="kpi-label">Restaurant records</div><div class="kpi-value" id="restaurantCount">—</div></div>
      <div class="kpi"><div class="kpi-label">Total revenue</div><div class="kpi-value" id="totalRevenue">—</div></div>
      <div class="kpi"><div class="kpi-label">Net profit</div><div class="kpi-value" id="totalProfit">—</div></div>
      <div class="kpi"><div class="kpi-label">Net margin</div><div class="kpi-value" id="totalMargin">—</div></div>
    </section>
    <div class="loss-note" id="lossNote" role="status"></div>

    <section class="charts" aria-label="Portfolio charts">
      <article class="panel"><h2>Revenue by operating format</h2><p class="panel-note">Aggregate revenue · filtered selection</p><div id="formatChart"></div></article>
      <article class="panel"><h2>Revenue channel mix</h2><p class="panel-note">Revenue by ordering channel</p><div class="donut-layout"><div class="donut" id="channelDonut" role="img" aria-label="Revenue channel mix chart"></div><div class="legend" id="channelLegend"></div></div></article>
    </section>
    <section class="dual" aria-label="Profitability and regional results">
      <article class="panel"><h2>Margin by operating format</h2><p class="panel-note">Aggregate profit divided by aggregate revenue</p><div id="marginChart"></div></article>
      <article class="panel"><h2>Revenue by subregion</h2><p class="panel-note">Aggregate revenue · filtered selection</p><div id="regionChart"></div></article>
    </section>

    <section class="panel table-section">
      <h2>Restaurant performance</h2>
      <div class="table-tools">
        <input id="searchInput" type="search" placeholder="Search restaurant, cuisine or subregion" aria-label="Search restaurants">
        <div class="table-count" id="tableCount"></div>
        <button id="downloadButton" type="button">Export filtered CSV</button>
      </div>
      <div class="table-wrap"><table><thead><tr><th>Restaurant</th><th>Cuisine</th><th>Format</th><th>Subregion</th><th>Monthly orders</th><th>Revenue</th><th>Net profit</th><th>Margin</th></tr></thead><tbody id="tableBody"></tbody></table></div>
    </section>
    <footer>Figures are calculated from the supplied channel revenue and net-profit fields. This self-contained HTML contains a data snapshot generated from the CSV; regenerate it after updating the source file. The figures are a portfolio diagnostic, not audited or verified sector-wide statistics.</footer>
  </main>
  <script>
    const SNAPSHOT = __DATA__;
    const records = SNAPSHOT.records;
    const channels = [
      {label: "In-store", revenue: "InStoreRevenue", color: "#155b58"},
      {label: "Uber Eats", revenue: "UberEatsRevenue", color: "#c7832f"},
      {label: "DoorDash", revenue: "DoorDashRevenue", color: "#427eaa"},
      {label: "Self-delivery", revenue: "SelfDeliveryRevenue", color: "#bd5b4c"},
    ];
    const formatColors = {"Full-service":"#155b58", "Cafe":"#c7832f", "QSR":"#427eaa", "Ghost Kitchen":"#bd5b4c"};
    const money = value => "$" + Number(value).toLocaleString("en-NZ", {maximumFractionDigits: 0});
    const compactMoney = value => "$" + (value / 1e6).toFixed(2) + "m";
    const number = value => Number(value).toLocaleString("en-NZ");
    const percent = value => (value * 100).toFixed(1) + "%";
    const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
    const controls = ["formatFilter", "regionFilter", "cuisineFilter", "profitFilter", "searchInput"];

    function fillOptions(id, values) {
      const select = document.getElementById(id);
      [...new Set(values)].sort((a, b) => a.localeCompare(b)).forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.append(option);
      });
    }
    fillOptions("formatFilter", records.map(row => row.Segment));
    fillOptions("regionFilter", records.map(row => row.Subregion));
    fillOptions("cuisineFilter", records.map(row => row.CuisineType));
    document.getElementById("generated").textContent = "Generated " + SNAPSHOT.generated;

    function selectedRows() {
      const format = document.getElementById("formatFilter").value;
      const region = document.getElementById("regionFilter").value;
      const cuisine = document.getElementById("cuisineFilter").value;
      const status = document.getElementById("profitFilter").value;
      const query = document.getElementById("searchInput").value.trim().toLocaleLowerCase();
      return records.filter(row =>
        (!format || row.Segment === format) &&
        (!region || row.Subregion === region) &&
        (!cuisine || row.CuisineType === cuisine) &&
        (status === "all" || (status === "loss" ? row.TotalProfit < 0 : row.TotalProfit >= 0)) &&
        (!query || [row.RestaurantName, row.CuisineType, row.Subregion, row.Segment].some(value => value.toLocaleLowerCase().includes(query)))
      );
    }

    function aggregate(rows, key) {
      const result = new Map();
      rows.forEach(row => {
        const entry = result.get(row[key]) || {name: row[key], revenue: 0, profit: 0};
        entry.revenue += row.TotalRevenue;
        entry.profit += row.TotalProfit;
        result.set(row[key], entry);
      });
      return [...result.values()];
    }

    function renderKpis(rows) {
      const revenue = rows.reduce((sum, row) => sum + row.TotalRevenue, 0);
      const profit = rows.reduce((sum, row) => sum + row.TotalProfit, 0);
      const losses = rows.filter(row => row.TotalProfit < 0).length;
      document.getElementById("restaurantCount").textContent = number(rows.length);
      document.getElementById("totalRevenue").textContent = compactMoney(revenue);
      document.getElementById("totalProfit").textContent = compactMoney(profit);
      document.getElementById("totalProfit").className = "kpi-value " + (profit < 0 ? "negative" : "positive");
      document.getElementById("totalMargin").textContent = percent(revenue ? profit / revenue : 0);
      document.getElementById("lossNote").textContent = rows.length
        ? `${number(losses)} of ${number(rows.length)} selected restaurant records (${percent(losses / rows.length)}) are loss-making.`
        : "No records match these filters. Adjust your selections.";
    }

    function renderFormat(rows) {
      const items = aggregate(rows, "Segment").sort((a, b) => b.revenue - a.revenue);
      const max = Math.max(...items.map(item => item.revenue), 1);
      document.getElementById("formatChart").innerHTML = items.length ? items.map(item => `
        <div class="bar-row"><span class="bar-name" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</span>
        <div class="track"><div class="fill" style="width:${(item.revenue / max * 100).toFixed(2)}%;background:${formatColors[item.name] || "#155b58"}"></div></div>
        <span class="bar-value">${compactMoney(item.revenue)}</span></div>`).join("") : '<div class="empty">No results</div>';
    }

    function renderChannels(rows) {
      const values = channels.map(channel => ({...channel, total: rows.reduce((sum, row) => sum + row[channel.revenue], 0)}));
      const total = values.reduce((sum, item) => sum + item.total, 0);
      let angle = 0;
      const slices = values.map(item => {
        const start = angle;
        angle += total ? item.total / total * 360 : 0;
        return `${item.color} ${start.toFixed(2)}deg ${angle.toFixed(2)}deg`;
      });
      document.getElementById("channelDonut").style.background = total
        ? `conic-gradient(${slices.join(",")})` : "#e7eeeb";
      document.getElementById("channelLegend").innerHTML = values.map(item => `
        <div class="legend-item"><span class="swatch" style="background:${item.color}"></span>
        <span>${item.label}</span><span class="legend-value">${total ? percent(item.total / total) : "0.0%"}</span></div>`).join("");
    }

    function renderMargins(rows) {
      const items = aggregate(rows, "Segment").map(item => ({...item, margin: item.revenue ? item.profit / item.revenue : 0}));
      const max = Math.max(...items.map(item => Math.abs(item.margin)), 0.01);
      document.getElementById("marginChart").innerHTML = items.sort((a, b) => a.margin - b.margin).map(item => {
        const width = Math.min(Math.abs(item.margin) / max * 48, 48);
        const left = item.margin < 0 ? 50 - width : 50;
        const color = item.margin < 0 ? "#bd5b4c" : "#155b58";
        return `<div class="margin-row"><div class="margin-caption"><span>${escapeHtml(item.name)}</span><span class="margin-number" style="color:${color}">${percent(item.margin)}</span></div>
        <div class="margin-track"><div class="margin-fill" style="left:${left}%;width:${width}%;background:${color}"></div></div></div>`;
      }).join("") || '<div class="empty">No results</div>';
    }

    function renderRegions(rows) {
      const items = aggregate(rows, "Subregion").sort((a, b) => b.revenue - a.revenue);
      const max = Math.max(...items.map(item => item.revenue), 1);
      document.getElementById("regionChart").innerHTML = items.map(item => `
        <div class="region-row"><div class="region-heading"><span>${escapeHtml(item.name)}</span><span class="bar-value">${compactMoney(item.revenue)}</span></div>
        <div class="track"><div class="fill" style="width:${(item.revenue / max * 100).toFixed(2)}%;background:#427eaa"></div></div></div>`).join("") || '<div class="empty">No results</div>';
    }

    function renderTable(rows) {
      const sorted = [...rows].sort((a, b) => b.TotalProfit - a.TotalProfit);
      const body = document.getElementById("tableBody");
      document.getElementById("tableCount").textContent = `Showing ${Math.min(sorted.length, 100)} of ${number(sorted.length)} records`;
      body.innerHTML = sorted.slice(0, 100).map(row => `<tr>
        <td>${escapeHtml(row.RestaurantName)}</td><td>${escapeHtml(row.CuisineType)}</td>
        <td>${escapeHtml(row.Segment)}</td><td>${escapeHtml(row.Subregion)}</td>
        <td class="numeric">${number(row.MonthlyOrders)}</td><td class="numeric">${money(row.TotalRevenue)}</td>
        <td class="numeric ${row.TotalProfit < 0 ? "negative" : "positive"}">${money(row.TotalProfit)}</td>
        <td class="numeric ${row.ProfitMargin < 0 ? "negative" : "positive"}">${percent(row.ProfitMargin)}</td></tr>`).join("") || '<tr><td class="empty" colspan="8">No restaurant records match the current filters.</td></tr>';
    }

    function render() {
      const rows = selectedRows();
      renderKpis(rows);
      renderFormat(rows);
      renderChannels(rows);
      renderMargins(rows);
      renderRegions(rows);
      renderTable(rows);
    }

    controls.forEach(id => document.getElementById(id).addEventListener("input", render));
    document.getElementById("resetButton").addEventListener("click", () => {
      controls.forEach(id => { document.getElementById(id).value = id === "profitFilter" ? "all" : ""; });
      render();
    });
    document.getElementById("downloadButton").addEventListener("click", () => {
      const rows = selectedRows();
      const columns = ["RestaurantName", "CuisineType", "Segment", "Subregion", "MonthlyOrders", "TotalRevenue", "TotalProfit", "ProfitMargin"];
      const csv = [columns.join(","), ...rows.map(row => columns.map(column => `"${String(row[column]).replaceAll('"', '""')}"`).join(","))].join("\r\n");
      const link = document.createElement("a");
      link.href = URL.createObjectURL(new Blob([csv], {type: "text/csv;charset=utf-8"}));
      link.download = "skycity_filtered_restaurants.csv";
      link.click();
      URL.revokeObjectURL(link.href);
    });
    render();
  </script>
</body>
</html>
'''

OUTPUT.write_text(html_template.replace("__DATA__", payload), encoding="utf-8")
print(f"Created {OUTPUT} with {len(records)} records")
