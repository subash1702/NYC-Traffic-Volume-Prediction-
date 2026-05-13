# NYC Traffic Volume Analytics Pipeline

An analytics pipeline on NYC's **Automated Traffic Volume Counts** (1.7M+ records) joined to the city's **Permitted Event Information** feed, with exploratory analysis and predictive models for two questions:

1. Does the presence of a permitted public event move traffic volume in that borough on that day?
2. Can we tell a weekday from a weekend using only volume, hour, and borough?

The answers turn out to be: *kind of, but you need more features* and *yes, but only with a non-linear model*.

---

## What's in here

| File | What it is |
|---|---|
| `traffic_analysis.py` | The pipeline as a module: load + clean, merge, EDA plots, regressor, classifiers |
| `notebooks/traffic_analysis.ipynb` | Thin notebook that imports the module and runs each stage in cells |
| `docs/final_report.pdf` | Full writeup with figures, methodology, and references |
| `docs/proposal.pdf` | Original project proposal |
| `docs/presentation.pptx` | Slide deck |

---

## Datasets

Both public, from NYC Open Data:

- [Automated Traffic Volume Counts](https://catalog.data.gov/dataset/traffic-volume-counts) — 1,712,605 records, 14 columns, 15-minute intervals
- [NYC Permitted Event Information – Historical](https://catalog.data.gov/dataset/nyc-permitted-event-information-historical)

Download both as CSV and place them in a local `data/` folder (gitignored).

---

## Quickstart

```bash
# 1. Create environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Update the two CSV paths inside the notebook (or at the bottom of traffic_analysis.py),
#    then either run the notebook end-to-end:
jupyter notebook notebooks/traffic_analysis.ipynb

#    or call the module directly:
python -c "import traffic_analysis as ta; \
           t, e = ta.load_and_clean_data('data/traffic.csv', 'data/events.csv'); \
           m = ta.merge_data(t, e); \
           ta.run_eda_plots(m); \
           ta.model_gbr(m); \
           ta.model_classifiers(m)"
```

---

## Pipeline

1. **Ingest** — read both CSVs with `pandas.read_csv`.
2. **Parse & clean** — build one `timestamp` from `Yr / M / D / HH / MM`, derive `hour_of_day`, `day_of_week`, `is_weekend`; normalize borough names (trim, title-case); drop rows missing volume or date.
3. **Sample** — 25,000 traffic rows + 2,500 event rows with `random_state=42` for reproducibility. Sampling here is for iteration speed, not statistical reasons.
4. **Merge** — left-join on `(event_day, borough)` so every traffic row keeps a flag `is_event_time` (True if a permitted event fell on that borough/day, False otherwise).
5. **EDA** — five plots: hourly profile, day-of-week, event vs non-event distribution, borough totals, hour×day heatmap.
6. **Model** — one regressor (volume), three classifiers (weekday vs weekend).

---

## What the models actually showed

### Volume prediction — Gradient Boosting Regressor

Features: `is_event_time`, `hour_of_day`, `day_of_week`.

| Metric | Value |
|---|---|
| R² | 0.07 |
| MSE | ≈ 30,472 |

Honest read: event *presence* alone isn't enough signal to predict volume. The variance you'd need to capture lives in features this dataset doesn't carry on its own — event *type*, expected attendance, venue proximity, and the specific street segment. The model isn't wrong; it's correctly reporting that the features given aren't sufficient.

### Weekday vs weekend — three classifiers

Features: `Vol`, `hour_of_day`, `Boro_code`. Target: `is_weekend`.

| Model | ROC-AUC | Notes |
|---|---:|---|
| Logistic Regression | 0.51 | Effectively random — the signal isn't linear in these features |
| **Random Forest** | **0.76** | Best balanced; picks up the interaction between hour and weekend |
| XGBoost | 0.71 | High overall accuracy, but recall on the weekend class drops to 0.24 |

Random Forest is the recommended model for this task on this feature set.

---

## Key findings from the data itself

The EDA actually carried more weight than the models:

- **Bimodal daily profile** — morning peak ~8 AM, evening peak ~4–5 PM, trough 1–4 AM. Visible on every weekday.
- **Day-of-week** — Thursday and Friday top weekdays; Sunday lowest.
- **Borough split** — Manhattan, Brooklyn, and Queens dominate total volume. Staten Island is roughly 1/5 of Queens.
- **Hour × day heatmap** — the bimodal pattern collapses on weekends into a flatter, lower curve. This is what the Random Forest is learning.

---

## Course context

ALY6140 — Python & Analytics Technology, Northeastern University.
Group 6: Moli Jangada & Subash Chakravarthy. Instructor: Prof. Daya Rudhramoorthi.

Full writeup with figures: [`docs/final_report.pdf`](docs/final_report.pdf).

---

## License

MIT.
