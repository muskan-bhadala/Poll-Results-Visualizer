from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
IMAGE_DIR = ROOT / "images"
RAW_FILE = DATA_DIR / "poll_data.csv"

def load_and_clean_data(path=RAW_FILE):
    df = pd.read_csv(path)
    required = ["Timestamp", "Age Group", "Region", "Gender", "Preferred Tool", "Satisfaction (1-5)", "Feedback"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")
    df = df.drop_duplicates().copy()
    for col in ["Age Group", "Region", "Gender", "Preferred Tool"]:
        df[col] = df[col].astype("string").str.strip()
    df["Preferred Tool"] = df["Preferred Tool"].str.title()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df["Satisfaction (1-5)"] = pd.to_numeric(df["Satisfaction (1-5)"], errors="coerce")
    df["Feedback"] = df["Feedback"].fillna("").astype(str).str.strip()
    df = df.dropna(subset=["Timestamp", "Preferred Tool", "Region", "Age Group", "Satisfaction (1-5)"])
    df = df[df["Satisfaction (1-5)"].between(1, 5)]
    df = df[df["Preferred Tool"].ne("")]
    df["Date"] = df["Timestamp"].dt.date.astype(str)
    df["Feedback Length"] = df["Feedback"].str.len()
    return df

def make_summary(df):
    summary = (df["Preferred Tool"].value_counts()
               .rename_axis("Option").reset_index(name="Votes"))
    total = int(summary["Votes"].sum())
    summary["Share (%)"] = (summary["Votes"] / total * 100).round(2) if total else 0
    return summary

def generate_outputs(df):
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)
    summary = make_summary(df)
    summary.to_csv(OUTPUT_DIR / "vote_share_summary.csv", index=False)
    df.to_csv(OUTPUT_DIR / "cleaned_poll_data.csv", index=False)
    region = pd.crosstab(df["Region"], df["Preferred Tool"])
    region.to_csv(OUTPUT_DIR / "region_preference_summary.csv")
    age = pd.crosstab(df["Age Group"], df["Preferred Tool"])
    age.to_csv(OUTPUT_DIR / "age_group_preference_summary.csv")

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=summary, x="Option", y="Votes", ax=ax)
    ax.set_title("Poll Votes by Preferred Tool")
    ax.set_xlabel("Preferred Tool"); ax.set_ylabel("Number of Votes")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "bar_chart.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(summary["Votes"], labels=summary["Option"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Share of Poll Responses")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "pie_chart.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(data=df, x="Region", hue="Preferred Tool", ax=ax)
    ax.set_title("Preferred Tool by Region"); ax.set_xlabel("Region"); ax.set_ylabel("Responses")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "region_comparison.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(data=df, x="Age Group", hue="Preferred Tool", ax=ax)
    ax.set_title("Preferred Tool by Age Group"); ax.set_xlabel("Age Group"); ax.set_ylabel("Responses")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "demographic_comparison.png", dpi=160); plt.close(fig)

    daily = df.groupby("Date").size().sort_index()
    fig, ax = plt.subplots(figsize=(9, 4))
    daily.plot(ax=ax, marker="o")
    ax.set_title("Poll Responses Over Time"); ax.set_xlabel("Date"); ax.set_ylabel("Responses")
    fig.autofmt_xdate(); fig.tight_layout()
    fig.savefig(IMAGE_DIR / "response_trend.png", dpi=160); plt.close(fig)

    comments = " ".join(df.loc[df["Feedback"].str.len() > 0, "Feedback"])
    if comments.strip():
        cloud = WordCloud(width=1000, height=500, background_color="white",
                          collocations=False, min_font_size=10).generate(comments)
        cloud.to_file(str(IMAGE_DIR / "feedback_wordcloud.png"))

    insights = []
    if not summary.empty:
        winner = summary.iloc[0]
        insights.append(f"Most preferred option: {winner['Option']} ({int(winner['Votes'])} votes, {winner['Share (%)']:.2f}% share).")
    insights.append(f"Valid responses analyzed: {len(df)}.")
    insights.append(f"Average satisfaction rating: {df['Satisfaction (1-5)'].mean():.2f}/5.")
    insights.append(f"Number of regions represented: {df['Region'].nunique()}.")
    (OUTPUT_DIR / "insights.txt").write_text("\\n".join(insights), encoding="utf-8")
    return summary, insights

def run_analysis():
    df = load_and_clean_data()
    summary, insights = generate_outputs(df)
    print(f"Loaded and cleaned {len(df)} responses.")
    print("\\nVote-share summary:")
    print(summary.to_string(index=False))
    print("\\nInsights:")
    print("\\n".join(f"- {line}" for line in insights))
    print(f"\\nReports saved in: {OUTPUT_DIR}")
    print(f"Charts saved in: {IMAGE_DIR}")
