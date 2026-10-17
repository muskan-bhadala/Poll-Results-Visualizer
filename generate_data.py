from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "poll_data.csv"
DATA.parent.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
n = 300
dates = pd.date_range("2026-09-15", periods=30, freq="D")
tools = ["Python", "Excel", "Power BI", "Tableau", "R"]
regions = ["North", "South", "East", "West"]
ages = ["18-24", "25-34", "35-44", "45+"]
genders = ["Female", "Male", "Prefer not to say"]
feedback_options = [
    "Easy to learn and useful for analysis",
    "Great tool for reports and dashboards",
    "Needs better documentation",
    "Helpful for visualizing data",
    "I prefer a simpler interface",
    "Very useful for my studies",
    "More features would be helpful",
    "Good for making decisions",
]
# Weighted synthetic distribution, not real survey findings.
tool = rng.choice(tools, n, p=[0.34, 0.24, 0.20, 0.14, 0.08])
df = pd.DataFrame({
    "Timestamp": rng.choice(dates, n) + pd.to_timedelta(rng.integers(0, 86400, n), unit="s"),
    "Age Group": rng.choice(ages, n, p=[0.42, 0.32, 0.17, 0.09]),
    "Region": rng.choice(regions, n),
    "Gender": rng.choice(genders, n, p=[0.47, 0.47, 0.06]),
    "Preferred Tool": tool,
    "Satisfaction (1-5)": rng.choice([1, 2, 3, 4, 5], n, p=[0.04, 0.09, 0.20, 0.38, 0.29]),
    "Feedback": rng.choice(feedback_options, n),
})
# Add a few intentional data-quality issues so cleaning can be demonstrated.
df.loc[4, "Preferred Tool"] = " python "
df.loc[10, "Feedback"] = ""
df.loc[20, "Satisfaction (1-5)"] = np.nan
df.to_csv(DATA, index=False)
print(f"Created synthetic dataset: {DATA}")
print(f"Rows: {len(df)}")
print(df.head().to_string(index=False))
