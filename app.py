"""Streamlit EDA dashboard for the HHS Unaccompanied Children dataset."""

from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"
DATE_COLUMN = "Date"
MEASURE_COLUMNS = {
    "Apprehended": "Children apprehended and placed in CBP custody*",
    "In CBP custody": "Children in CBP custody",
    "Transferred out": "Children transferred out of CBP custody",
    "In HHS care": "Children in HHS Care",
    "Discharged": "Children discharged from HHS Care",
}

# Color palette for consistent, distinguishable chart colors
CHART_COLORS = {
    "Apprehended": "#1f77b4",       # blue
    "In CBP custody": "#d62728",    # red
    "Transferred out": "#ff7f0e",   # orange
    "In HHS care": "#2ca02c",       # green
    "Discharged": "#9467bd",        # purple
}


@st.cache_data
def load_data(uploaded_file=None) -> pd.DataFrame:
    """Load, validate, and sort the supplied operational extract."""
    source = uploaded_file if uploaded_file is not None else DATA_PATH
    frame = pd.read_csv(source)
    required = {DATE_COLUMN, *MEASURE_COLUMNS.values()}
    missing = required.difference(frame.columns)
    if missing:
        missing_names = ", ".join(sorted(missing))
        raise ValueError(f"CSV is missing required columns: {missing_names}")

    frame[DATE_COLUMN] = pd.to_datetime(frame[DATE_COLUMN], errors="coerce")
    if frame[DATE_COLUMN].isna().any():
        raise ValueError("CSV contains invalid or missing dates.")
    for column in MEASURE_COLUMNS.values():
        frame[column] = (
            frame[column].astype(str).str.replace(",", "", regex=False).pipe(pd.to_numeric, errors="coerce")
        )
    if frame[list(MEASURE_COLUMNS.values())].isna().any().any():
        raise ValueError("CSV contains invalid or missing numeric values.")
    return frame.sort_values(DATE_COLUMN).reset_index(drop=True)


def render_chart_with_selection(
    filtered: pd.DataFrame,
    available_metrics: list,
    section_key: str,
    default_selections: list = None,
) -> None:
    """Render a line chart with a dropdown/multiselect for metric selection and a chart-type toggle."""
    if default_selections is None:
        default_selections = available_metrics

    col_select, col_chart_type = st.columns([3, 1])

    with col_select:
        selected = st.multiselect(
            "Select metrics to display",
            options=available_metrics,
            default=default_selections,
            key=f"{section_key}_metrics",
        )

    with col_chart_type:
        chart_type = st.selectbox(
            "Chart type",
            options=["Line", "Area", "Bar"],
            index=0,
            key=f"{section_key}_chart_type",
        )

    if not selected:
        st.info("Select at least one metric from the dropdown above.")
        return

    # Build chart data with short names
    raw_cols = [MEASURE_COLUMNS[name] for name in selected]
    chart_data = (
        filtered.set_index(DATE_COLUMN)[raw_cols]
        .rename(columns={MEASURE_COLUMNS[k]: k for k in selected})
    )

    # Render the chosen chart type
    color_list = [CHART_COLORS[name] for name in selected]
    if chart_type == "Line":
        st.line_chart(chart_data, color=color_list)
    elif chart_type == "Area":
        st.area_chart(chart_data, color=color_list)
    else:
        st.bar_chart(chart_data, color=color_list)

    # Show individual sparklines when multiple metrics are selected
    if len(selected) > 1:
        with st.expander("View individual metric charts", expanded=False):
            for name in selected:
                st.markdown(f"**{name}**")
                single_col = [MEASURE_COLUMNS[name]]
                single_data = (
                    filtered.set_index(DATE_COLUMN)[single_col]
                    .rename(columns={MEASURE_COLUMNS[name]: name})
                )
                st.line_chart(single_data, color=[CHART_COLORS[name]], height=200)


def main() -> None:
    st.set_page_config(page_title="HHS Unaccompanied Children EDA", layout="wide")
    st.title("HHS Unaccompanied Children Program: Exploratory Data Analysis")
    st.caption(
        "Descriptive operational snapshots only. Missing dates are not interpreted as zero activity, "
        "and totals are not unique-child counts."
    )

    # -- Sidebar ---------------------------------------------------------------
    st.sidebar.header("Controls")
    uploaded_file = st.sidebar.file_uploader("Upload a compatible CSV", type="csv")
    try:
        data = load_data(uploaded_file)
    except FileNotFoundError:
        st.info("Upload the HHS CSV to begin. The default path is data/HHS_Unaccompanied_Alien_Children_Program.csv.")
        st.stop()
    except ValueError as error:
        st.error(str(error))
        st.stop()

    min_date = data[DATE_COLUMN].min().date()
    max_date = data[DATE_COLUMN].max().date()
    selected_dates = st.sidebar.date_input(
        "Observation date range",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered = data[data[DATE_COLUMN].dt.date.between(start_date, end_date)].copy()
    else:
        filtered = data.copy()
    if filtered.empty:
        st.warning("No observations match the selected date range.")
        st.stop()

    # -- KPI Cards -------------------------------------------------------------
    care_column = MEASURE_COLUMNS["In HHS care"]
    latest = filtered.iloc[-1]
    latest_care = int(latest[care_column])
    peak_row = data.loc[data[care_column].idxmax()]
    care_change = (latest_care / peak_row[care_column] - 1) * 100
    kpi_columns = st.columns(4)
    kpi_columns[0].metric("Latest HHS care", f"{latest_care:,}", latest[DATE_COLUMN].strftime("%b %d, %Y"))
    kpi_columns[1].metric("Peak HHS care", f"{int(peak_row[care_column]):,}", peak_row[DATE_COLUMN].strftime("%b %d, %Y"))
    kpi_columns[2].metric("Observations", f"{len(filtered):,}")
    kpi_columns[3].metric("Latest vs. peak", f"{care_change:.1f}%")

    st.divider()

    # -- HHS Care Population Chart ---------------------------------------------
    st.subheader("HHS Care Population")
    st.caption("Track the number of children in HHS care over time. Use the dropdown to overlay related metrics.")
    render_chart_with_selection(
        filtered,
        available_metrics=["In HHS care", "Discharged"],
        section_key="hhs_care",
        default_selections=["In HHS care"],
    )

    st.divider()

    # -- Operational Flows Chart -----------------------------------------------
    st.subheader("Operational Flows")
    st.caption(
        "Compare CBP apprehension, custody, transfer, and discharge flows. "
        "Select individual metrics or combine them."
    )
    flow_metrics = ["Apprehended", "In CBP custody", "Transferred out", "Discharged"]
    render_chart_with_selection(
        filtered,
        available_metrics=flow_metrics,
        section_key="operational_flows",
        default_selections=flow_metrics,
    )

    st.divider()

    # -- All Metrics Combined --------------------------------------------------
    st.subheader("Custom Metric Explorer")
    st.caption("Build your own comparison by selecting any combination of available metrics.")
    all_metrics = list(MEASURE_COLUMNS.keys())
    render_chart_with_selection(
        filtered,
        available_metrics=all_metrics,
        section_key="custom_explorer",
        default_selections=[],
    )

    st.divider()

    # -- Summary Statistics & Data Quality -------------------------------------
    left, right = st.columns(2)
    with left:
        st.subheader("Distribution of Measures")
        summary = filtered[list(MEASURE_COLUMNS.values())].describe().T
        summary.index = MEASURE_COLUMNS.keys()
        st.dataframe(
            summary[["count", "mean", "50%", "min", "max"]]
            .rename(columns={"50%": "median"})
            .round(1)
        )
    with right:
        st.subheader("Data-Quality Checks")
        flow_columns = [MEASURE_COLUMNS[name] for name in flow_metrics]
        duplicate_dates = int(filtered[DATE_COLUMN].duplicated().sum())
        observed_days = (filtered[DATE_COLUMN].max() - filtered[DATE_COLUMN].min()).days + 1
        st.write(f"- Duplicate dates: **{duplicate_dates}**")
        st.write(f"- Observed span: **{observed_days:,}** calendar days")
        st.write(f"- Missing calendar days in span: **{max(observed_days - len(filtered), 0):,}**")
        st.write(
            "- Numeric values below zero: **"
            + str(int((filtered[flow_columns + [care_column]] < 0).sum().sum()))
            + "**"
        )

    st.divider()

    # -- Source Records --------------------------------------------------------
    st.subheader("Source Records")
    st.dataframe(filtered, use_container_width=True)


if __name__ == "__main__":
    main()
