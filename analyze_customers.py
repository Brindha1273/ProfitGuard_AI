
import pandas as pd

# Load the synthetic B2B customer dataset
df = pd.read_csv("b2b_customers.csv")

# Calculate a transparent, rule-based churn-risk score
def calculate_churn_risk(row):
    score = 0

    if row["days_since_last_order"] > 90:
        score += 40
    elif row["days_since_last_order"] > 60:
        score += 25

    if row["complaints_last_year"] >= 5:
        score += 25
    elif row["complaints_last_year"] >= 3:
        score += 15

    if row["satisfaction_score"] <= 2:
        score += 25
    elif row["satisfaction_score"] == 3:
        score += 10

    if row["orders_last_year"] <= 5:
        score += 10

    return min(score, 100)

df["churn_risk_score"] = df.apply(calculate_churn_risk, axis=1)

def risk_category(score):
    if score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    return "Low"

df["risk_category"] = df["churn_risk_score"].apply(risk_category)

# Estimate annual contribution margin using an illustrative 25% margin
df["estimated_contribution_margin"] = (
    df["annual_revenue"] * 0.25
).round(2)

# Rank high-risk accounts by estimated contribution margin
df = df.sort_values(
    ["risk_category", "estimated_contribution_margin"],
    ascending=[True, False]
)

df.to_csv("customer_analytics.csv", index=False)

print("Customer analytics completed!")
print("\nRisk category counts:")
print(df["risk_category"].value_counts())

print("\nTop 10 accounts to review:")
print(
    df[[
        "customer_id",
        "company_name",
        "churn_risk_score",
        "risk_category",
        "estimated_contribution_margin"
    ]].head(10).to_string(index=False)
)

print("\nSaved results to customer_analytics.csv")
