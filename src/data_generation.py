import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Setup

np.random.seed(42)

# Create monthly date range (4 years)
months = pd.date_range(start="2020-01-01", periods=48, freq="ME")

starting_customers = 1000
subscription_price = 50
base_churn_rate = 0.05

data = []
active_customers = starting_customers

# Generate SaaS Revenue Data
for month in months:

    # Seasonality in customer acquisition
    seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * month.month / 12)

    new_customers = int(np.random.normal(120, 15) * seasonal_factor)

    churn_rate = base_churn_rate + np.random.normal(0, 0.005)

    # Prevent negative churn rate
    churn_rate = max(churn_rate, 0.01)

    churned_customers = int(active_customers * churn_rate)

    active_customers = active_customers + new_customers - churned_customers

    mrr = active_customers * subscription_price

    data.append([
        month,
        new_customers,
        churn_rate,
        churned_customers,
        active_customers,
        subscription_price,
        mrr
    ])


# Create DataFrame

columns = [
    "Month",
    "New_Customers",
    "Churn_Rate",
    "Churned_Customers",
    "Active_Customers",
    "Subscription_Price",
    "MRR"
]

df = pd.DataFrame(data, columns=columns)

# Derived Metrics
df["Revenue_Growth_%"] = df["MRR"].pct_change() * 100
df["Customer_Growth_%"] = df["Active_Customers"].pct_change() * 100

# Summary Statistics
print(df.head())
print("\nAverage Churn Rate:", round(df["Churn_Rate"].mean(), 4))
print("Average Monthly Revenue Growth %:", round(df["Revenue_Growth_%"].mean(), 2))

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(df["Month"], df["MRR"])
plt.title("Monthly Recurring Revenue (MRR)")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()
