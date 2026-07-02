# Customer Churn Analysis & Prediction

**Can we predict which telecom customers are about to leave — and what should the business do about it?**

This project combines exploratory analysis, feature engineering, and machine learning to identify the key drivers of customer churn and build a model that flags at-risk customers before they leave.

---

## Result at a glance

| Driver | Finding |
|--------|---------|
| Contract type | Month-to-month customers churn at **42.7%** vs **2.8%** for two-year contracts — a 14x difference |
| Tenure | Customers in their first 12 months churn at **~2x** the rate of established customers |
| Monthly charges | Churners pay **$13/month more** on average ($74.44 vs $61.31) |
| Payment method | Electronic check payers churn at **45.3%** vs **~15–17%** for auto-pay methods |
| Internet service | Fiber optic customers churn at **41.9%** vs **19%** for DSL |

### Model performance

| Model | ROC-AUC | Churn Recall | Churn Precision |
|-------|---------|-------------|----------------|
| Logistic Regression | **0.833** | **0.79** | 0.49 |
| Random Forest | 0.818 | 0.49 | 0.62 |

**Logistic Regression recommended for deployment** — higher ROC-AUC and significantly better churn recall (0.79 vs 0.49), meaning it catches nearly twice as many at-risk customers.

---

## What this project covers

- **Data cleaning** — fixed `TotalCharges` type issue (whitespace strings coerced to NaN, 11 rows dropped); encoded target variable as binary
- **EDA** — analyzed churn rates across contract type, tenure, monthly charges, internet service, and payment method with visualizations
- **Feature engineering** — created `is_new_customer` (tenure ≤ 12 months) and `avg_monthly_spend` grounded in EDA findings
- **Modeling** — logistic regression and random forest with `class_weight='balanced'` to handle the 74/26 class imbalance
- **Evaluation** — confusion matrix, classification report, ROC-AUC comparison
- **Business recommendations** — five concrete retention actions derived from the analysis

---

## Business Recommendations

**1. Prioritize contract upgrades**
Incentivize month-to-month customers to move to one-year contracts. The ~40 percentage point reduction in churn risk easily justifies a moderate discount.

**2. Build a 90-day onboarding program**
The first 12 months are the highest-risk window. Proactive check-ins and early engagement touchpoints can meaningfully reduce early churn.

**3. Incentivize auto-pay at signup**
Electronic check payers churn at nearly 3x the rate of auto-pay customers. A small incentive ($5/month off) for enrolling in automatic payment could reduce churn significantly.

**4. Investigate fiber optic service quality**
Fiber customers pay more and churn more — a value perception problem. A targeted NPS survey of this segment is a logical next step.

**5. Deploy model as a monthly risk score**
Use the Logistic Regression model (ROC-AUC 0.833) to score customers monthly and route the top at-risk accounts to the retention team for proactive outreach.

---

## Files

```
├── churn_analysis.ipynb    # Full analysis: EDA → feature engineering → modeling → recommendations
└── README.md
```

> **Note:** The dataset is not included in this repo. Download `WA_Fn-UseC_-Telco-Customer-Churn.csv` from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn), place it in the project folder, and rename it `telco_churn.csv`.

---

## How to run

```bash
git clone https://github.com/Deepti-Dhanapala/customer-churn-analysis.git
cd customer-churn-analysis
pip install pandas numpy matplotlib seaborn scikit-learn
jupyter notebook churn_analysis.ipynb
```

---

## Tech stack

- **Language:** Python 3
- **Libraries:** pandas, numpy, matplotlib, seaborn, scikit-learn

---

## 🤖 AI-Powered Churn Assistant

Built an interactive AI assistant on top of this analysis using the Claude API and Streamlit.

### What it does
- Loads and analyzes the churn dataset automatically
- Calculates key business metrics (churn rate, contract breakdown, payment method analysis)
- Allows users to ask any business question in plain English
- Claude answers with specific data-backed insights and recommendations

### Tech Stack
- Python, Pandas — data processing
- Anthropic Claude API — AI-powered analysis
- Streamlit — interactive web dashboard

### Files
- `churn_assistant.py` — terminal-based Q&A assistant
- `app.py` — Streamlit web dashboard

### How to Run
```bash
pip install anthropic pandas streamlit python-dotenv
# Add your Anthropic API key to .env file
streamlit run app.py
```

## About me

I'm a data scientist with a Master of Professional Studies (MPS) in Data Science from the University at Buffalo (graduated Feb 2026), actively looking for Data Scientist, Product Data Scientist, and Data Analyst roles.

[LinkedIn](https://linkedin.com/in/deeptidhanpal) · [GitHub](https://github.com/Deepti-Dhanapala)
