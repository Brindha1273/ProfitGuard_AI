
import pandas as pd
import random

random.seed(42)

industries = [
    "Manufacturing",
    "Healthcare",
    "Education",
    "Hospitality",
    "Retail"
]

customers = []

for i in range(1, 101):
    recency_days = random.randint(1, 180)
    orders = random.randint(2, 40)
    avg_order_value = random.randint(5000, 50000)
    complaints = random.randint(0, 8)
    satisfaction = random.randint(1, 5)

    customers.append({
        "customer_id": f"CUST{i:03d}",
        "company_name": f"Company {i:03d}",
        "industry": random.choice(industries),
        "days_since_last_order": recency_days,
        "orders_last_year": orders,
        "average_order_value": avg_order_value,
        "annual_revenue": orders * avg_order_value,
        "complaints_last_year": complaints,
        "satisfaction_score": satisfaction,
        "discount_rate": round(random.uniform(0, 0.20), 2),
        "account_manager_contacted": random.choice(["Yes", "No"])
    })

df = pd.DataFrame(customers)

df.to_csv("b2b_customers.csv", index=False)

print("ProfitGuard AI dataset created successfully!")
print(f"Total customers: {len(df)}")
print("\nFirst five customers:")
print(df.head())
print("\nDataset saved as b2b_customers.csv")
