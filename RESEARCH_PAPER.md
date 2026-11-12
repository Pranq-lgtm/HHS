# Operational Patterns in the HHS Unaccompanied Children Program

## Abstract

This paper provides an exploratory analysis of the supplied public HHS Unaccompanied Children Program extract. The file contains 720 timestamped observations from January 12, 2023 through December 21, 2025 and five operational measures: children apprehended and placed in CBP custody, children in CBP custody, children transferred out of CBP custody, children in HHS care, and children discharged from HHS care. The analysis identifies a large change in program scale over the observation window, substantial volatility in flows, and a lower but persistent HHS-care population by late 2025. These findings support capacity planning, exception monitoring, and better publication of data-quality metadata; they do not establish causal relationships or measure individual child outcomes.

## 1. Research questions

1. How did the observed HHS-care population change over the study period?
2. What patterns are visible in apprehension, custody-transfer, and discharge flows?
3. What operational actions can government stakeholders take without over-interpreting the descriptive data?

## 2. Data and methodology

### Source and scope

The analysis uses `data/HHS_Unaccompanied_Alien_Children_Program.csv`, supplied with this project and attributed to [HHS.gov](https://www.hhs.gov/). The extract has 720 rows spanning 1,075 calendar days. There are fewer records than calendar days, so the file should be treated as a periodic operational snapshot rather than a complete daily time series.

### Preparation

- Dates were parsed from the text field `Month day, year`.
- Numeric fields were converted after removing thousands separators.
- Records were sorted chronologically.
- Totals and averages are descriptive calculations over reported observations; they are not population estimates for unobserved days.
- No imputation, smoothing, causal modeling, or demographic inference was applied.

### Measures

| Measure | Interpretation |
|---|---|
| Apprehended | Children apprehended and placed in CBP custody |
| In CBP custody | Reported CBP custody count |
| Transferred out | Children transferred out of CBP custody |
| In HHS care | Reported HHS care count |
| Discharged | Children discharged from HHS care |

## 3. Exploratory findings

### 3.1 Overall scale and distribution

| Measure | Observed total | Mean per observation | Median | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| Apprehended | 67,337 | 93.5 | 99 | 0 | 333 |
| In CBP custody | 123,476 | 171.5 | 193 | 7 | 531 |
| Transferred out | 92,641 | 128.7 | 157 | 0 | 440 |
| In HHS care | 4,364,118 | 6,061.3 | 6,406.5 | 1,972 | 11,516 |
| Discharged | 124,853 | 173.4 | 181 | 0 | 505 |

The median exceeding the mean for CBP custody, transfers out, and HHS care indicates that lower observations pull the average down. The wide ranges show that planning from a single average would obscure high-volume periods.

### 3.2 HHS-care population

The maximum reported HHS-care population is 11,516 on December 20, 2023. The final observation, December 21, 2025, reports 2,484 children in HHS care. The endpoint is approximately 77% below the observed maximum. This is a descriptive comparison of two reported snapshots, not a claim that the program followed a smooth decline.

The series is volatile: the high point occurs late in 2023, falls through much of 2024, and remains near 2,000–2,500 in the late-2025 observations. A capacity model should therefore use rolling ranges and scenario bands rather than only the full-period mean of 6,061.

### 3.3 Flows and operational pressure

- The largest apprehension observation is 333 children on February 15, 2024.
- The largest CBP-custody observation is 531 on February 4, 2024.
- The largest transfer-out observation is 440 on February 12, 2024.
- The largest discharge observation is 505 on August 31, 2023.
- Across all reported observations, transfers out total 92,641 compared with 123,476 in CBP custody, a difference of -30,835. These fields are not necessarily paired cohorts or a balance sheet, so the difference should not be read as a backlog calculation.

The proximity of several February 2024 maxima suggests an interval that merits operational review. The dataset alone cannot identify the cause; stakeholders would need policy, weather, border, facility, and case-management context.

### 3.4 Data quality observations

The reporting cadence is irregular: 720 observations cover 1,075 calendar days. Some calendar periods have only a handful of observations. The extract also lacks facility, state, age, sex, referral, discharge destination, length-of-stay, and denominator fields. Consequently:

- totals are sums of observations, not unique children;
- a zero may mean a reported zero, while a missing date means no observation, not necessarily zero activity;
- aggregate data cannot support individual-level conclusions;
- cross-series arithmetic should not be treated as a formal stock-and-flow reconciliation without definitions and timing rules.

## 4. Implications for government stakeholders

1. **Capacity:** The range from 1,972 to 11,516 children in HHS care implies a need for surge capacity and a baseline operating plan.
2. **Early warning:** Apprehensions, CBP custody, transfers, and discharges should be monitored together because pressure can appear in one measure before another.
3. **Timeliness:** High-volume observations deserve same-week review of placement capacity, transportation, staffing, and case-processing throughput.
4. **Transparency:** Publication should include cadence, revision history, field definitions, and whether values are point-in-time counts or event totals.
5. **Equity and safeguards:** Any operational dashboard should protect children’s privacy and avoid publishing personally identifiable information or small-cell data.

## 5. Recommendations

### Immediate (0–90 days)

- Establish a weekly operational review using the dashboard and a documented exception threshold.
- Add data-quality checks for duplicate dates, missing dates, unexpected negatives, and schema changes.
- Maintain a rolling 30-observation median and 90th percentile for HHS care, apprehensions, and discharges.
- Annotate major policy or reporting changes directly in the time series.

### Near term (3–12 months)

- Publish a machine-readable data dictionary and a stable release identifier.
- Add facility-level capacity, occupied beds, placements pending, length-of-stay, and discharge pathway fields where privacy and policy permit.
- Reconcile the timing definitions for custody and transfer measures before presenting them as a flow balance.
- Build a forecast with prediction intervals and explicit missing-observation handling.

### Longer term

- Evaluate operational interventions with pre-specified metrics rather than relying on before/after visual comparisons.
- Create privacy-preserving geographic and demographic aggregates for equity monitoring.
- Conduct independent validation of data lineage from source systems to public release.

## 6. Limitations

This is an exploratory descriptive study. It does not estimate causal effects, forecast future demand, evaluate program quality, or represent all children served. The supplied extract may be revised by its source. Because observation dates are irregular and field definitions are limited, totals should not be interpreted as unique-child counts or as a complete accounting of program movement.

## 7. Reproducibility

The Streamlit dashboard's `app.py` and the Colab-compatible `EDA_HHS_Unaccompanied_Children.ipynb` parse the same CSV and calculate the displayed KPIs and charts from the supplied file. The paper's summary statistics can be reproduced by sorting `Date`, removing commas from numeric fields, and applying ordinary count, sum, mean, median, minimum, and maximum functions.

**Prepared for:** Government and program-operations stakeholders  
**Source:** [U.S. Department of Health & Human Services](https://www.hhs.gov/)
