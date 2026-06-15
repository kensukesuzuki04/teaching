"""
ECON10 — Regional Labor Market in the US
Data: BLS LAUS la.data.3.AllStatesS (Seasonally Adjusted State Unemployment Rates)

Run this script to load, clean, and visualize the data.
Outputs are saved to the output/ folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px

def show_plotly(fig):
    """Try VS Code Interactive Window first, then safe fallbacks."""
    try:
        fig.show(renderer="vscode")
    except Exception:
        try:
            fig.show(renderer="notebook_connected")
        except Exception:
            fig.show(renderer="browser")

# ── 1. Load raw data ──────────────────────────────────────────────────────────

df = pd.read_csv(
    "data/la.data.3.AllStatesS.txt",
    sep="\t",
    skipinitialspace=True
)
df.columns = df.columns.str.strip()
df["series_id"] = df["series_id"].str.strip()

# Keep only unemployment rate series (code 003).
df = df[df["series_id"].str.endswith("003")].copy()

# Sanity check: fail fast if any non-003 series slips in.
if not df["series_id"].str.endswith("003").all():
    raise ValueError("Non-003 series found after filtering. Stop and inspect the data pipeline.")

print(f"Using series suffix: {sorted(df['series_id'].str[-3:].unique().tolist())}")

print(f"Loaded {len(df):,} rows")
print(df.head())

# ── 2. Clean data ─────────────────────────────────────────────────────────────

# Extract 2-digit state FIPS code from series_id (positions 5–6)
df["state_fips"] = df["series_id"].str[5:7]

# FIPS → state name and abbreviation lookup tables
fips_to_name = {
    "01": "Alabama",        "02": "Alaska",         "04": "Arizona",
    "05": "Arkansas",       "06": "California",     "08": "Colorado",
    "09": "Connecticut",    "10": "Delaware",        "11": "District of Columbia",
    "12": "Florida",        "13": "Georgia",         "15": "Hawaii",
    "16": "Idaho",          "17": "Illinois",        "18": "Indiana",
    "19": "Iowa",           "20": "Kansas",          "21": "Kentucky",
    "22": "Louisiana",      "23": "Maine",           "24": "Maryland",
    "25": "Massachusetts",  "26": "Michigan",        "27": "Minnesota",
    "28": "Mississippi",    "29": "Missouri",        "30": "Montana",
    "31": "Nebraska",       "32": "Nevada",          "33": "New Hampshire",
    "34": "New Jersey",     "35": "New Mexico",      "36": "New York",
    "37": "North Carolina", "38": "North Dakota",    "39": "Ohio",
    "40": "Oklahoma",       "41": "Oregon",          "42": "Pennsylvania",
    "44": "Rhode Island",   "45": "South Carolina",  "46": "South Dakota",
    "47": "Tennessee",      "48": "Texas",           "49": "Utah",
    "50": "Vermont",        "51": "Virginia",        "53": "Washington",
    "54": "West Virginia",  "55": "Wisconsin",       "56": "Wyoming",
    "72": "Puerto Rico"
}
fips_to_abbr = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO",
    "09": "CT", "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI",
    "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
    "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
    "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
    "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD",
    "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
    "54": "WV", "55": "WI", "56": "WY", "72": "PR"
}

df["state"] = df["state_fips"].map(fips_to_name)
df["state_abbr"] = df["state_fips"].map(fips_to_abbr)
df = df.dropna(subset=["state"])

# Parse date
df["month"] = df["period"].str[1:].astype(int)
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
df = df.rename(columns={"value": "unemployment_rate"})

# Convert to numeric — BLS files sometimes have trailing spaces or footnote codes
df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")

df_clean = df[["state", "state_abbr", "state_fips", "date", "year", "month", "unemployment_rate"]].copy()
df_clean = df_clean.sort_values(["state", "date"]).reset_index(drop=True)

print(f"\nDate range: {df_clean['date'].min().strftime('%B %Y')} → {df_clean['date'].max().strftime('%B %Y')}")
print(f"States: {df_clean['state'].nunique()}")

# ── 3. Chart: National average trend ─────────────────────────────────────────

national_avg = df_clean.groupby("date")["unemployment_rate"].mean().reset_index()
national_avg.columns = ["date", "avg_unemployment"]

# Some recent months can contain suppressed values for many states.
# Keep only months with broad coverage to avoid artificial spikes.
state_coverage = (
    df_clean.dropna(subset=["unemployment_rate"])
    .groupby("date")["state_abbr"]
    .nunique()
    .reset_index(name="n_states")
)
valid_dates = state_coverage[state_coverage["n_states"] >= 50]["date"]
national_avg = national_avg[national_avg["date"].isin(valid_dates)].copy()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(national_avg["date"], national_avg["avg_unemployment"],
        color="#1f77b4", linewidth=1.5)

ax.set_title("U.S. State-Level Average Unemployment Rate (1976–Present)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Unemployment Rate (%)")
ax.xaxis.set_major_locator(mdates.YearLocator(5))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("output/national_trend.png", dpi=150)
plt.show()
print("Saved: output/national_trend.png")

# ── 4. Chart: All states interactive line chart with region filters ──────────

regions = {
    "Northeast": [
        "Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont",
        "New Jersey", "New York", "Pennsylvania"
    ],
    "South": [
        "Delaware", "District of Columbia", "Florida", "Georgia", "Maryland", "North Carolina",
        "South Carolina", "Virginia", "West Virginia", "Alabama", "Kentucky", "Mississippi",
        "Tennessee", "Arkansas", "Louisiana", "Oklahoma", "Texas"
    ],
    "Midwest": [
        "Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin", "Iowa", "Kansas", "Minnesota",
        "Missouri", "Nebraska", "North Dakota", "South Dakota"
    ]
}

df_lines = df_clean.copy()

fig_lines = px.line(
    df_lines,
    x="date", y="unemployment_rate", color="state",
    title="Monthly Unemployment Rate — All States (Seasonally Adjusted)",
    labels={"date": "Date", "unemployment_rate": "Unemployment Rate (%)", "state": "State"},
    template="plotly_white"
)

trace_names = [trace.name for trace in fig_lines.data]

def visible_mask(state_names):
    return [name in state_names for name in trace_names]

all_states_mask = [True] * len(trace_names)
ne_mask = visible_mask(regions["Northeast"])
south_mask = visible_mask(regions["South"])
midwest_mask = visible_mask(regions["Midwest"])

fig_lines.update_layout(
    hovermode="x unified",
    legend_title_text="State",
    updatemenus=[
        {
            "type": "buttons",
            "direction": "right",
            "x": 0,
            "y": 1.18,
            "showactive": True,
            "buttons": [
                {"label": "All", "method": "update", "args": [{"visible": all_states_mask}]},
                {"label": "Northeast", "method": "update", "args": [{"visible": ne_mask}]},
                {"label": "South", "method": "update", "args": [{"visible": south_mask}]},
                {"label": "Midwest", "method": "update", "args": [{"visible": midwest_mask}]}
            ]
        }
    ]
)
show_plotly(fig_lines)

# ── 5. Maps: Static comparisons ──────────────────────────────────────────────

first_complete_date = state_coverage[state_coverage["n_states"] >= 50]["date"].min()
latest_complete_date = state_coverage[state_coverage["n_states"] >= 50]["date"].max()
df_latest = df_clean[df_clean["date"] == latest_complete_date].copy()
df_first = df_clean[df_clean["date"] == first_complete_date].copy()
print(f"\nLatest complete data: {latest_complete_date.strftime('%B %Y')}")

# 5a) Latest unemployment rate by state
fig_map_static = px.choropleth(
    df_latest,
    locations="state_abbr",
    locationmode="USA-states",
    color="unemployment_rate",
    scope="usa",
    color_continuous_scale="RdYlGn_r",
    range_color=[2, 8],
    title=f"State Unemployment Rates — {latest_complete_date.strftime('%B %Y')} (Seasonally Adjusted)",
    labels={"unemployment_rate": "Unemployment Rate (%)"}
)
show_plotly(fig_map_static)
fig_map_static.write_image("output/map_latest_static.png", width=1000, height=600)
print("Saved: output/map_latest_static.png")

# 5b) Change from oldest complete month to latest complete month
df_change_long = df_latest[["state", "state_abbr", "unemployment_rate"]].merge(
    df_first[["state_abbr", "unemployment_rate"]],
    on="state_abbr",
    how="inner",
    suffixes=("_latest", "_first")
)
df_change_long["change_pp"] = df_change_long["unemployment_rate_latest"] - df_change_long["unemployment_rate_first"]

fig_change_long = px.choropleth(
    df_change_long,
    locations="state_abbr",
    locationmode="USA-states",
    color="change_pp",
    scope="usa",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    range_color=[-6, 6],
    title=(
        "Change in State Unemployment Rate "
        f"({first_complete_date.strftime('%b %Y')} to {latest_complete_date.strftime('%b %Y')})"
    ),
    labels={"change_pp": "Change (percentage points)"}
)
show_plotly(fig_change_long)
fig_change_long.write_image("output/map_change_oldest_to_latest.png", width=1000, height=600)
print("Saved: output/map_change_oldest_to_latest.png")

# 5c) COVID recovery map: 2024 annual average minus 2021 annual average
year_start = 2021
year_end = 2024
df_annual_recovery = (
    df_clean[df_clean["year"].isin([year_start, year_end])]
    .groupby(["state", "state_abbr", "year"])["unemployment_rate"]
    .mean()
    .reset_index()
)

rec_start = (
    df_annual_recovery[df_annual_recovery["year"] == year_start]
    [["state_abbr", "unemployment_rate"]]
    .rename(columns={"unemployment_rate": "rate_start"})
)
rec_end = (
    df_annual_recovery[df_annual_recovery["year"] == year_end]
    [["state", "state_abbr", "unemployment_rate"]]
    .rename(columns={"unemployment_rate": "rate_end"})
)
df_recovery = rec_end.merge(rec_start, on="state_abbr", how="inner")
df_recovery["change_pp"] = df_recovery["rate_end"] - df_recovery["rate_start"]

fig_recovery = px.choropleth(
    df_recovery,
    locations="state_abbr",
    locationmode="USA-states",
    color="change_pp",
    scope="usa",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    range_color=[-4, 4],
    title="State Unemployment Rate Change: 2021 to 2024 (Annual Average)",
    labels={"change_pp": "2024 - 2021 (pp)"}
)
show_plotly(fig_recovery)
fig_recovery.write_image("output/map_change_2021_2024.png", width=1000, height=600)
print("Saved: output/map_change_2021_2024.png")

# 5d) Relative to Massachusetts in the latest complete month
ma_rate = df_latest.loc[df_latest["state_abbr"] == "MA", "unemployment_rate"].iloc[0]
df_vs_ma = df_latest[["state", "state_abbr", "unemployment_rate"]].copy()
df_vs_ma["diff_vs_ma_pp"] = df_vs_ma["unemployment_rate"] - ma_rate

fig_vs_ma = px.choropleth(
    df_vs_ma,
    locations="state_abbr",
    locationmode="USA-states",
    color="diff_vs_ma_pp",
    scope="usa",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    range_color=[-4, 4],
    title=(
        "Unemployment Rate Relative to Massachusetts "
        f"({latest_complete_date.strftime('%b %Y')})"
    ),
    labels={"diff_vs_ma_pp": "State - MA (pp)"}
)
show_plotly(fig_vs_ma)
fig_vs_ma.write_image("output/map_relative_to_ma.png", width=1000, height=600)
print("Saved: output/map_relative_to_ma.png")

# ── 6. Map: Annual average with year slider (interactive) ─────────────────────

df_annual = df_clean[df_clean["year"] >= 1990].copy()
df_annual_avg = df_annual.groupby(["state", "state_abbr", "year"])["unemployment_rate"].mean().reset_index()
df_annual_avg["unemployment_rate"] = df_annual_avg["unemployment_rate"].round(1)

fig_map_interactive = px.choropleth(
    df_annual_avg,
    locations="state_abbr",
    locationmode="USA-states",
    color="unemployment_rate",
    animation_frame="year",
    scope="usa",
    color_continuous_scale="RdYlGn_r",
    range_color=[2, 12],
    title="Annual Average State Unemployment Rates (1990–Present)",
    labels={"unemployment_rate": "Unemployment Rate (%)"}
)
fig_map_interactive.update_layout(coloraxis_colorbar=dict(title="Rate (%)"))
show_plotly(fig_map_interactive)

print("\nDone! Check the output/ folder for saved images.")
