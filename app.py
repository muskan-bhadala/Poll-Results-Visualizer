from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from src.analysis import load_and_clean_data, make_summary, generate_outputs, ROOT

st.set_page_config(page_title="Poll Results Visualizer", page_icon="📊", layout="wide")
st.title("📊 Poll Results Visualizer")
st.caption("Explore poll preferences, satisfaction ratings, demographic differences, and written feedback.")
default_path = ROOT / "data" / "poll_data.csv"

uploaded = st.sidebar.file_uploader("Upload your poll CSV", type=["csv"])
if uploaded:
    raw = pd.read_csv(uploaded)
    # Save upload to a temporary project data file for reuse by the same cleaning pipeline.
    df = raw.copy()
    required = ["Timestamp", "Age Group", "Region", "Gender", "Preferred Tool", "Satisfaction (1-5)", "Feedback"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error("CSV needs these columns: " + ", ".join(required))
        st.stop()
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
else:
    df = load_and_clean_data(default_path)

if df.empty:
    st.warning("No valid responses are available after cleaning.")
    st.stop()

st.sidebar.header("Filters")
regions = sorted(df["Region"].dropna().unique().tolist())
ages = sorted(df["Age Group"].dropna().unique().tolist())
options = sorted(df["Preferred Tool"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_ages = st.sidebar.multiselect("Age group", ages, default=ages)
selected_options = st.sidebar.multiselect("Preferred tool", options, default=options)
filtered = df[df["Region"].isin(selected_regions) & df["Age Group"].isin(selected_ages) & df["Preferred Tool"].isin(selected_options)]
if filtered.empty:
    st.warning("No rows match the current filters. Select at least one region, age group, and tool.")
    st.stop()

summary = make_summary(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Valid Responses", f"{len(filtered):,}")
c2.metric("Options", filtered["Preferred Tool"].nunique())
c3.metric("Average Satisfaction", f"{filtered['Satisfaction (1-5)'].mean():.2f}/5")
c4.metric("Top Option", str(summary.iloc[0]["Option"]) if not summary.empty else "N/A")

st.subheader("Vote Share Summary")
st.dataframe(summary, use_container_width=True, hide_index=True)
st.download_button("Download vote-share summary CSV", summary.to_csv(index=False).encode("utf-8"), "vote_share_summary.csv", "text/csv")

left, right = st.columns(2)
with left:
    st.subheader("Votes by Preferred Tool")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=summary, x="Option", y="Votes", ax=ax)
    ax.tick_params(axis="x", rotation=25)
    ax.set_xlabel("Preferred Tool"); ax.set_ylabel("Votes")
    st.pyplot(fig); plt.close(fig)
with right:
    st.subheader("Percentage Share")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(summary["Votes"], labels=summary["Option"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig); plt.close(fig)

st.subheader("Regional Comparison")
region_table = pd.crosstab(filtered["Region"], filtered["Preferred Tool"])
st.bar_chart(region_table)
st.subheader("Age-Group Comparison")
age_table = pd.crosstab(filtered["Age Group"], filtered["Preferred Tool"])
st.bar_chart(age_table)

st.subheader("Satisfaction Ratings")
rating_counts = filtered["Satisfaction (1-5)"].value_counts().sort_index()
st.bar_chart(rating_counts)

st.subheader("Responses Over Time")
daily = filtered.groupby(filtered["Timestamp"].dt.date).size().sort_index()
st.line_chart(daily)

st.subheader("Feedback Word Cloud")
feedback = " ".join(filtered.loc[filtered["Feedback"].str.len() > 0, "Feedback"])
if feedback.strip():
    cloud = WordCloud(width=1000, height=450, background_color="white", collocations=False).generate(feedback)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(cloud, interpolation="bilinear"); ax.axis("off")
    st.pyplot(fig); plt.close(fig)
else:
    st.info("No written feedback is available for this selection.")

st.subheader("Generated Insights")
st.write(f"- **Leading option:** {summary.iloc[0]['Option']} with {int(summary.iloc[0]['Votes'])} votes ({summary.iloc[0]['Share (%)']:.2f}% of filtered responses).")
st.write(f"- **Average satisfaction:** {filtered['Satisfaction (1-5)'].mean():.2f} out of 5.")
st.write(f"- **Regions represented:** {filtered['Region'].nunique()}.")
with st.expander("View filtered response data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered cleaned data", filtered.to_csv(index=False).encode("utf-8"), "filtered_cleaned_poll_data.csv", "text/csv")
st.caption("Demo data is synthetic and for learning only. It does not represent real public opinion.")
