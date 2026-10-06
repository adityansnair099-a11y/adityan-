# SkyCity Auckland Restaurant Portfolio: Exploratory Data Analysis, Insights, and Recommendations

## Abstract

This paper examines 1,696 restaurant records in the supplied SkyCity Auckland Restaurants & Bars dataset. Recalculated channel totals produce $77.74 million in recorded revenue and $7.87 million in net profit, an aggregate margin of 10.1%. Portfolio performance varies sharply by operating format: Full-service has a negative aggregate margin, while Cafe, Ghost Kitchen, and QSR are positive. Uber Eats and DoorDash together account for 61.2% of recorded revenue but have a combined calculated net margin below 1%. These findings identify areas for investigation, not causal effects. The dataset does not specify its currency, reporting period, provenance, or profit-allocation method, so results should be treated as a descriptive portfolio diagnostic rather than verified sector-wide evidence.

## 1. Research Questions

1. What do the supplied records show about revenue and net profitability across formats, regions, and channels?
2. Where are the largest differences in recorded unit economics?
3. What additional analysis and operational responses are justified by the evidence?

## 2. Data and Method

The source file contains 1,696 records and 33 columns. Restaurant IDs are unique in this extract, and the file has no missing cells. Fields cover cuisine, format, subregion, monthly orders, average order value, channel revenue, cost rates, delivery costs, and channel net profit.

For this analysis, total revenue is the sum of in-store, Uber Eats, DoorDash, and self-delivery revenue. Total net profit is the sum of the corresponding four channel net-profit fields. Aggregate margin is total net profit divided by total revenue. Segment and regional margins are calculated from each group's aggregate profit and revenue, not by averaging individual record margins. Channel margin is each channel's summed net profit divided by its summed revenue.

## 3. Exploratory Findings

### Portfolio distribution

The portfolio records $77.74 million in revenue and $7.87 million in net profit, for a 10.1% aggregate margin. Of the 1,696 records, 408 (24.1%) have negative total net profit. Median recorded revenue is $44,686 and median net profit is $4,933. Average monthly orders are about 1,191 per record, and average order value is $38.52. Monetary units and the period represented by these figures are not stated in the source.

### Performance by operating format

| Format | Records | Revenue | Net profit | Aggregate margin | Loss-making records |
|---|---:|---:|---:|---:|---:|
| Cafe | 504 | $23.25m | $3.77m | 16.2% | 0 |
| Full-service | 452 | $22.59m | -$1.30m | -5.8% | 408 |
| Ghost Kitchen | 197 | $8.03m | $1.78m | 22.2% | 0 |
| QSR | 543 | $23.87m | $3.61m | 15.1% | 0 |

All loss-making records in this extract are classified as Full-service. That is a notable concentration for follow-up, but does not establish why the losses occur. The result may depend on how channel costs and shared operating expenses are allocated in the underlying data.

### Performance by channel

| Channel | Revenue | Net profit | Calculated margin |
|---|---:|---:|---:|
| In-store | $14.28m | $3.83m | 26.8% |
| Uber Eats | $30.82m | $0.26m | 0.8% |
| DoorDash | $16.79m | $0.15m | 0.9% |
| Self-delivery | $15.85m | $3.63m | 22.9% |

Uber Eats and DoorDash together account for 61.2% of recorded revenue and $409,610 in calculated net profit, a combined margin of 0.86%. This is a substantial gap from the calculated in-store and self-delivery margins. It is an association in the supplied accounting fields, not evidence that platform use or commissions alone cause lower profit.

### Regional variation

Aggregate margins range from 9.5% in the CBD to 10.5% in West Auckland. South Auckland records a 10.2% margin and North Shore 10.1%. The margins are relatively close compared with the difference between operating formats. Regional results are descriptive and do not control for format, cuisine, or outlet-level cost differences.

## 4. Interpretation

The positive portfolio-wide margin masks concentrated losses: a single format accounts for every loss-making record and has negative aggregate profit. Channel revenue volume also does not correspond to channel profitability in the supplied figures; the third-party platforms generate most recorded revenue but very little net profit. In-store and self-delivery have stronger calculated margins, although the source does not document whether costs are allocated consistently across channels.

The data supports prioritizing format- and channel-level investigation. It does not support a causal claim about delivery platforms, a forecast of future performance, or general conclusions about Auckland's hospitality sector. The `GrowthFactor` field has no accompanying time series or definition and is not treated here as observed growth.

## 5. Recommendations

1. **Review Full-service economics at record level.** Reconcile the 408 loss-making records against sales mix, food and labor costs, rent, delivery cost, and overhead allocation. Identify viable changes before considering broad-based support or exit decisions.
2. **Audit channel contribution calculations.** Confirm that commissions, refunds, promotions, packaging, delivery costs, and shared labor are consistently attributed. Recalculate contribution per order using a common definition across channels.
3. **Test platform improvements with measured pilots.** Assess menu pricing, product availability, basket design, and commission terms using controlled before-and-after comparisons. Track net contribution, order volume, and customer retention rather than revenue alone.
4. **Protect stronger economics while checking scalability.** Examine the in-store and self-delivery results for replicable practices, while testing whether additional volume changes labor, delivery, or service costs.
5. **Improve the evidence base for public decisions.** Add reporting period, currency, provenance, and formula definitions; maintain comparable time-series data; and collect employment, wages, business survival, local procurement, and neighborhood outcomes before evaluating wider public benefits.

## 6. Limitations

The source does not identify its reporting period, currency, data provenance, representativeness, or calculation methodology. Net-profit figures are accepted as supplied and are not independently audited. No time series, employment, wage, tax, local-spending, or customer-level variables are provided. Accordingly, the findings describe this file only and should not be presented as causal estimates or as representative statistics for the wider restaurant sector.

## Conclusion

The supplied portfolio data shows positive aggregate profitability alongside material format- and channel-level variation. The most immediate analytical priority is to validate and understand Full-service losses and very low third-party platform margins. Sound operational or government decisions will require verified cost definitions and broader evidence than this single, undated extract provides.
