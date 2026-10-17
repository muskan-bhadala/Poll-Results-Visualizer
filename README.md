# Poll Results Visualizer

An interactive Python and Streamlit dashboard that cleans poll/survey responses, calculates vote shares, compares demographic groups, visualizes trends, and summarizes feedback.

> **Dataset note:** The included dataset is synthetically generated for demonstration. Its results are not real-world survey findings.

## Features
- Generate reproducible sample poll data
- Clean duplicates, text categories, timestamps, and satisfaction ratings
- Calculate vote counts and percentage shares
- Compare preferences by region and age group
- Visualize results with bar, pie, comparison, rating, and trend charts
- Explore written feedback with a word cloud
- Upload compatible CSV data through the dashboard
- Download vote-share and cleaned-data CSV reports
- Generate reusable charts and text insights

## Tech stack
Python, Pandas, NumPy, Matplotlib, Seaborn, Streamlit, WordCloud.

## Project structure
```text
Poll-Results-Visualizer/
├── data/
│   └── poll_data.csv
├── images/
│   └── (generated charts go here)
├── notebooks/
├── outputs/
│   └── (generated CSV reports and insights go here)
├── src/
│   ├── __init__.py
│   └── analysis.py
├── app.py
├── generate_data.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup (Windows PowerShell)
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python generate_data.py
python main.py
streamlit run app.py
```
If Python 3.13 is not installed, use `py -m venv .venv` and activate the environment.

If PowerShell blocks activation for this session, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## CSV format for uploaded surveys
The dashboard expects these columns:
- `Timestamp`
- `Age Group`
- `Region`
- `Gender`
- `Preferred Tool`
- `Satisfaction (1-5)`
- `Feedback`

You can export Google Forms responses as CSV and rename/map columns to this format. Do not upload personally identifiable or confidential survey data to a public repository.

## Outputs
Running `python main.py` creates:
- `outputs/cleaned_poll_data.csv`
- `outputs/vote_share_summary.csv`
- `outputs/region_preference_summary.csv`
- `outputs/age_group_preference_summary.csv`
- `outputs/insights.txt`
- Charts in `images/`

## Screenshot checklist
Save your own screenshots from the running application:
1. `images/dashboard-overview.png`
2. `images/vote-share-summary.png`
3. `images/region-comparison.png`
4. `images/age-group-comparison.png`
5. `images/feedback-wordcloud.png`
6. `images/github-repository.png`

## Limitations
Synthetic data demonstrates the pipeline but cannot support conclusions about actual populations. Small groups, sampling bias, missing responses, and survey wording can affect interpretation.

## Future improvements
- Sentiment analysis for open-ended feedback
- Live polling/API integration
- More flexible question types and CSV column mapping
- Power BI integration
- Deployment to Streamlit Community Cloud

## License
MIT (add a `LICENSE` file if you choose to distribute under the MIT License).
