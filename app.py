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


def main() -> None:
    st.set_page_config(page_title="HHS Unaccompanied Children EDA", layout="wide")
    st.title("HHS Unaccompanied Children Program: Exploratory Data Analysis")
    st.caption(
        "Descriptive operational snapshots only. Missing dates are not interpreted as zero activity, "
        "and totals are not unique-child counts."
    )

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
    selected_dates = st.sidebar.date_input("Observation date range", (min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered = data[data[DATE_COLUMN].dt.date.between(start_date, end_date)].copy()
    else:
        filtered = data.copy()
    if filtered.empty:
        st.warning("No observations match the selected date range.")
        st.stop()

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

    st.subheader("HHS care population")
    care_chart = filtered.set_index(DATE_COLUMN)[[care_column]].rename(columns={care_column: "Children"})
    st.line_chart(care_chart)

    st.subheader("Operational flows")
    flow_columns = [MEASURE_COLUMNS[name] for name in ("Apprehended", "In CBP custody", "Transferred out", "Discharged")]
    st.line_chart(filtered.set_index(DATE_COLUMN)[flow_columns].rename(columns={value: key for key, value in MEASURE_COLUMNS.items()}))

    left, right = st.columns(2)
    with left:
        st.subheader("Distribution of measures")
        summary = filtered[list(MEASURE_COLUMNS.values())].describe().T
        summary.index = MEASURE_COLUMNS.keys()
        st.dataframe(summary[["count", "mean", "50%", "min", "max"]].rename(columns={"50%": "median"}).round(1))
    with right:
        st.subheader("Data-quality checks")
        duplicate_dates = int(filtered[DATE_COLUMN].duplicated().sum())
        observed_days = (filtered[DATE_COLUMN].max() - filtered[DATE_COLUMN].min()).days + 1
        st.write(f"- Duplicate dates: **{duplicate_dates}**")
        st.write(f"- Observed span: **{observed_days:,}** calendar days")
        st.write(f"- Missing calendar days in span: **{max(observed_days - len(filtered), 0):,}**")
        st.write("- Numeric values below zero: **" + str(int((filtered[flow_columns + [care_column]] < 0).sum().sum())) + "**")

    st.subheader("Source records")
    st.dataframe(filtered, use_container_width=True)


if __name__ == "__main__":
    main()
