# HHS Unaccompanied Children Program Dashboard

This project is a lightweight, dependency-free dashboard for the public HHS Unaccompanied Children Program dataset.

## Run locally

Because browsers block `fetch()` for local files, serve the folder with any static server, for example:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000` in a browser. The dashboard loads the included CSV automatically. Use **Load another CSV** to explore an updated export with the same columns.

## Included views

- Latest children in HHS care
- Average daily apprehensions
- Total discharges and net custody movement
- Daily HHS-care trend and custody-flow charts
- Date range filtering and source-record table

## Research deliverables

- [Research paper: EDA, insights, recommendations](./RESEARCH_PAPER.md)
- [Executive summary for government stakeholders](./EXECUTIVE_SUMMARY.md)
- [Colab-compatible EDA notebook](./EDA_HHS_Unaccompanied_Children.ipynb)

## Streamlit app

Install the Python dependencies and start the EDA dashboard:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

The app reads `data/HHS_Unaccompanied_Alien_Children_Program.csv` when present. If the file is not present, upload a compatible CSV from the sidebar. The notebook uses the same fallback behavior in Google Colab.

Source: [HHS.gov](https://www.hhs.gov/).
