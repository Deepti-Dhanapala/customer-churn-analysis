import pandas as pd
import anthropic

#load the dataset
df = pd.read_csv("telco_churn.csv")

#Quick check 
print("Dataset loaded successfully.!")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\nFirst 3 rows:")
print(df.head(3))

# Calculate key stastistics from data
total_customers = len(df)
churn_rate = (df['Churn'].value_counts()['Yes'] / total_customers * 100).round(2)
avg_monthly_charges_mean = df['MonthlyCharges'].mean().round(2)
avg_monthly_charges_median = df['MonthlyCharges'].median().round(2)
avg_tenure = df['tenure'].mean().round(2)

#Churn rate by contract type 
contract_churn = df.groupby('Contract')['Churn'].apply(
    lambda x: (x== 'Yes').sum() / len(x) * 100
).round(2)

#Churn rate by payment menthod
payment_churn = df.groupby('PaymentMethod')['Churn'].apply(
    lambda x: (x== 'Yes').sum() / len(x) * 100
).round(2)

#Build a summary string
data_summary = f"""
TELECOM CUSTOMER CHURN DATASET SUMMARY:
- Total Customers: {total_customers}
- Overall Churn Rate: {churn_rate}%
- Average monthly charges (mean): ${avg_monthly_charges_mean}
- Average monthly charges (median): ${avg_monthly_charges_median}
- Average Tenure: {avg_tenure} months

Churn Rate by Contract Type:
{contract_churn.to_string()}

Churn Rate by Payment Method:
{payment_churn.to_string()}
"""
print(data_summary)

import os
from dotenv import load_dotenv
load_dotenv()
# Connect to Claude API and ask questions
client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")


def ask_claude(question):
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a data analyst assistant. 
Here is a summary of a telecom customer churn dataset:

{data_summary}

Answer this question based on the data above:
{question}

Be specific, reference the actual numbers, and give actionable insights."""
            }
        ]
    )
    return message.content[0].text

# Interactive Q&A loop
print("\n" + "="*50)
print("CHURN DATA ASSISTANT - Ask me anything!")
print("Type 'quit' to exit")
print("="*50)

while True:
    user_question = input("\nYour question: ")
    
    if user_question.lower() == 'quit':
        print("Goodbye!")
        break
    
    if user_question.strip() == "":
        print("Please enter a question!")
        continue
    
    print("\nAnalyzing...")
    print("\nClaude's Answer:")
    print(ask_claude(user_question))
    print("\n" + "-"*50)