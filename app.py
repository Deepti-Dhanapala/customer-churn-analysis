import streamlit as st
import pandas as pd
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Churn Data Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Churn AI Assistant")
st.write("Ask any business question about the telecom churn dataset")

# ---- RATE LIMITING ----
DEMO_LIMIT = 2

if "ai_calls" not in st.session_state:
    st.session_state.ai_calls = 0

@st.cache_data
def load_data():
    df = pd.read_csv("telco_churn.csv")
    return df

df = load_data()

total_customers = len(df)
churn_rate = (df['Churn'].value_counts()['Yes'] / total_customers * 100).round(2)
avg_monthly_mean = df['MonthlyCharges'].mean().round(2)
avg_monthly_median = df['MonthlyCharges'].median().round(2)
avg_tenure = df['tenure'].mean().round(2)

contract_churn = df.groupby('Contract')['Churn'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100
).round(2)
payment_churn = df.groupby('PaymentMethod')['Churn'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100
).round(2)

data_summary = f"""
TELECOM CUSTOMER CHURN DATASET SUMMARY:
- Total customers: {total_customers}
- Overall churn rate: {churn_rate}%
- Average monthly charges (mean): ${avg_monthly_mean}
- Average monthly charges (median): ${avg_monthly_median}
- Average tenure: {avg_tenure} months
Churn rate by contract type:
{contract_churn.to_string()}
Churn rate by payment method:
{payment_churn.to_string()}
"""

st.subheader("📈 Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", f"{total_customers:,}")
with col2:
    st.metric("Churn Rate", f"{churn_rate}%")
with col3:
    st.metric("Avg Monthly (Mean)", f"${avg_monthly_mean}")
with col4:
    st.metric("Avg Tenure", f"{avg_tenure} months")

st.subheader("📋 Churn Breakdown")
col1, col2 = st.columns(2)
with col1:
    st.write("**By Contract Type:**")
    st.dataframe(contract_churn.reset_index().rename(columns={'Churn': 'Churn Rate (%)'}))
with col2:
    st.write("**By Payment Method:**")
    st.dataframe(payment_churn.reset_index().rename(columns={'Churn': 'Churn Rate (%)'}))

st.subheader("💬 Ask Claude About Your Data")
st.write("Type a business question and Claude will answer using the dataset above")

remaining = DEMO_LIMIT - st.session_state.ai_calls
st.info(f"🔢 Demo limit: {remaining} of {DEMO_LIMIT} questions remaining this session")

question = st.text_input(
    "Your question:",
    placeholder="e.g. Which customer segment has the highest churn risk?"
)

if st.button("Ask Claude") and question:
    if st.session_state.ai_calls >= DEMO_LIMIT:
        st.warning(
            "⚠️ You've reached the 2-question demo limit. "
            "Clone the repo and add your own Anthropic API key to continue exploring!"
        )
    else:
        with st.spinner("Analyzing..."):
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are a data analyst assistant.
Here is a summary of a telecom customer churn dataset:
{data_summary}
Answer this question based on the data above:
{question}
Be specific, reference actual numbers, and give actionable insights."""
                    }
                ]
            )
            answer = message.content[0].text

        st.session_state.ai_calls += 1
        st.subheader("Claude's Answer:")
        st.markdown(answer)