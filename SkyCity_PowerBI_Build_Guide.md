# SkyCity Auckland Restaurant Portfolio — Power BI build guide

This guide recreates the portfolio dashboard in Power BI Desktop using the
provided Excel export. It specifies the model, DAX, visuals, formatting, and
validation checks.

## 1. Load the data

1. Open Power BI Desktop and choose **Home > Get data > Excel workbook**.
2. Select `SkyCity_Auckland_Restaurants_For_PowerBI.xlsx` from the project
   folder.
3. In Navigator, select the worksheet containing the restaurant rows and choose
   **Transform Data**.
4. In Power Query, rename the query to **Portfolio**. Confirm that the first row
   is used as headers and set the types:
   - Text: `CuisineType`, `RestaurantName`, `Segment`, `Subregion`
   - Whole number: `RestaurantID`, `MonthlyOrders`
   - Decimal number: all revenue, profit, rate, share, order-count, and cost
     fields
5. Choose **Close & Apply**.
6. In Model view, confirm the imported table is named **Portfolio**. This table
   name is used in all formulas below. No relationships are needed for this
   single-table report.

The source has one row per restaurant. The revenue and profit fields are
channel-level fields; the total fields used below are calculated from them.

## 2. Add calculated columns

In Data or Model view, select the `Portfolio` table, choose **New column**, and
create each column separately:

```DAX
TotalRevenue =
    COALESCE ( 'Portfolio'[InStoreRevenue], 0 )
        + COALESCE ( 'Portfolio'[UberEatsRevenue], 0 )
        + COALESCE ( 'Portfolio'[DoorDashRevenue], 0 )
        + COALESCE ( 'Portfolio'[SelfDeliveryRevenue], 0 )
```

```DAX
TotalProfit =
    COALESCE ( 'Portfolio'[InStoreNetProfit], 0 )
        + COALESCE ( 'Portfolio'[UberEatsNetProfit], 0 )
        + COALESCE ( 'Portfolio'[DoorDashNetProfit], 0 )
        + COALESCE ( 'Portfolio'[SelfDeliveryNetProfit], 0 )
```

```DAX
ProfitMargin =
    DIVIDE ( 'Portfolio'[TotalProfit], 'Portfolio'[TotalRevenue] )
```

```DAX
ProfitStatus =
    IF ( 'Portfolio'[TotalProfit] < 0, "Loss-making", "Profitable" )
```

Set `ProfitMargin` to **Percentage** with one decimal place. Set `TotalRevenue`
and `TotalProfit` to **Decimal number** with a thousands separator and two
decimal places. The source does not specify its currency, so do not assign a
currency symbol unless that has been confirmed.

## 3. Add measures

Select **Modeling > New measure** and add the following measures to `Portfolio`.
Create them one at a time.

```DAX
Restaurants =
    COUNTROWS ( 'Portfolio' )
```

```DAX
Revenue =
    SUM ( 'Portfolio'[TotalRevenue] )
```

```DAX
Net Profit =
    SUM ( 'Portfolio'[TotalProfit] )
```

```DAX
Profit Margin =
    DIVIDE ( [Net Profit], [Revenue] )
```

```DAX
Loss-making Restaurants =
    CALCULATE (
        [Restaurants],
        KEEPFILTERS ( 'Portfolio'[ProfitStatus] = "Loss-making" )
    )
```

```DAX
Loss-making Share =
    DIVIDE ( [Loss-making Restaurants], [Restaurants] )
```

```DAX
Loss-making Summary =
    FORMAT ( [Loss-making Restaurants], "#,0" )
        & " selected restaurants ("
        & FORMAT ( [Loss-making Share], "0.0%" )
        & ") are loss-making."
```

Format `Profit Margin` and `Loss-making Share` as percentages with one decimal
place.

## 4. Add the channel table and measures

The four channel revenues are separate source columns. A small disconnected
table lets a single donut chart display them as categories while still
responding to the report slicers.

Choose **Modeling > New table**:

```DAX
Channels =
    DATATABLE (
        "Channel", STRING,
        {
            { "In-store" },
            { "Uber Eats" },
            { "DoorDash" },
            { "Self-delivery" }
        }
    )
```

Do not create a relationship from `Channels` to `Portfolio`. Then create these
measures:

```DAX
Channel Revenue =
    SWITCH (
        SELECTEDVALUE ( 'Channels'[Channel] ),
        "In-store", SUM ( 'Portfolio'[InStoreRevenue] ),
        "Uber Eats", SUM ( 'Portfolio'[UberEatsRevenue] ),
        "DoorDash", SUM ( 'Portfolio'[DoorDashRevenue] ),
        "Self-delivery", SUM ( 'Portfolio'[SelfDeliveryRevenue] ),
        BLANK ()
    )
```

```DAX
Channel Share =
    DIVIDE (
        [Channel Revenue],
        CALCULATE ( [Revenue], REMOVEFILTERS ( 'Channels' ) )
    )
```

## 5. Build the report page

Use one **16:9** report page. Arrange it as a filter rail on the left and
dashboard canvas on the right. Choose **View > Themes > Customize current
theme** and use:

| Use | Color |
| --- | --- |
| Page background | `#F4F7F5` |
| Main text | `#203238` |
| Muted text | `#66777A` |
| Pine green | `#155B58` |
| Ochre | `#C7832F` |
| Blue | `#427EAA` |
| Coral | `#BD5B4C` |
| Card background | `#FFFFFF` |

### Header

- Add a text box at the top: **SkyCity Auckland | Restaurant Portfolio**
- Add a smaller subtitle: **Interactive analytics from the local source data**
- Add a note near the title or page footer: **Source currency is unspecified.**

### Slicers

Place four slicers in the left rail, in this order:

1. `Portfolio[Segment]` — title **Format**
2. `Portfolio[Subregion]` — title **Subregion**
3. `Portfolio[CuisineType]` — title **Cuisine**
4. `Portfolio[ProfitStatus]` — title **Profit status**

For each slicer, enable **Select all** if available. Clearing its selection
means all values are included. Use dropdown style for the first three and a
horizontal tile/list style for Profit status if it fits. Keep slicer
interactions enabled so the slicers filter each other and all visuals.

### KPI cards

Place four Card visuals across the top of the main canvas:

| Card title | Field |
| --- | --- |
| Restaurants | `[Restaurants]` |
| Revenue | `[Revenue]` |
| Net profit | `[Net Profit]` |
| Profit margin | `[Profit Margin]` |

Use display units **Millions** for Revenue and Net profit if supported, with
two decimals. Because the currency is unknown, use a number format rather than
assuming dollars. Use one decimal place for Profit margin.

Under the KPI cards, add a Card visual using `[Loss-making Summary]`. Give it a
subtle blue background or accent. With all filters cleared, it should read:
**408 selected restaurants (24.1%) are loss-making.**

### Visuals

Arrange these four visuals in a two-column grid below the banner:

| Visual title | Power BI visual | Fields and settings |
| --- | --- | --- |
| Revenue by operating format | Clustered bar chart | Y-axis: `Portfolio[Segment]`; X-axis/Values: `[Revenue]`; Tooltips: `[Net Profit]`, `[Revenue]`; sort by `[Revenue]` ascending to match the original chart. |
| Channel revenue mix | Donut chart | Legend: `Channels[Channel]`; Values: `[Channel Revenue]`; Tooltips: `[Channel Revenue]`, `[Channel Share]`; hole size about 60%. |
| Profit margin by format | Clustered bar chart | Y-axis: `Portfolio[Segment]`; X-axis/Values: `[Profit Margin]`; Tooltips: `[Revenue]`, `[Net Profit]`, `[Profit Margin]`; sort by `[Profit Margin]` ascending. Format the axis as percentage. |
| Revenue and margin by subregion | Scatter chart | X-axis: `[Revenue]`; Y-axis: `[Profit Margin]`; Size: `[Revenue]`; Details: `Portfolio[Subregion]`; Tooltips: `[Net Profit]`, `[Profit Margin]`. If the Power BI version offers a Legend bucket, use `Portfolio[Subregion]` there as well. Format Y-axis as percentage. |

Use these data colors in the same order for the channel donut:

- In-store: `#155B58`
- Uber Eats: `#C7832F`
- DoorDash: `#427EAA`
- Self-delivery: `#BD5B4C`

For Revenue by operating format, assign distinct palette colors by segment.
For Profit margin by format, enable conditional data colors using coral for
lower margin, ochre in the middle, and pine green for higher margin.

At the bottom of the page, add a Table visual titled **Restaurant performance**
with these fields in order:

1. `Portfolio[RestaurantName]`
2. `Portfolio[CuisineType]`
3. `Portfolio[Segment]`
4. `Portfolio[Subregion]`
5. `Portfolio[MonthlyOrders]`
6. `Portfolio[TotalRevenue]`
7. `Portfolio[TotalProfit]`
8. `Portfolio[ProfitMargin]`

Sort the table by `TotalProfit` descending. Format `ProfitMargin` as a
percentage and revenue/profit as numbers with two decimal places.

## 6. Validate the report

With no filters selected, check that the report returns approximately:

| Check | Expected |
| --- | ---: |
| Restaurant rows | 1,696 |
| Revenue | 77,739,306.80 |
| Net profit | 7,866,306.13 |
| Profit margin | 10.1% |
| Loss-making restaurants | 408 |
| Loss-making share | 24.1% |

The exact source values are summarized without imposing a currency. Rounding
or Power BI display-unit settings can change only the displayed precision.
Changing `Profit status` to **Loss-making** should reduce the restaurant count
to 408 and show a 100.0% loss-making share. Changing it to **Profitable** should
show zero loss-making restaurants.

## 7. Save and refresh

1. Choose **File > Save as** and save the report as
   `SkyCity_Auckland_Portfolio.pbix`.
2. The report reads from the Excel file at its current path. If the file is
   moved, update the source under **Transform data > Data source settings**.
3. Use **Home > Refresh** after replacing or updating the workbook.

This guide creates a native Power BI report when followed in Power BI Desktop;
the HTML mockup and the Excel workbook are not themselves `.pbix` files.
