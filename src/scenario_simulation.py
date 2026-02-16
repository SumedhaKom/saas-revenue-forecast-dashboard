import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

months = pd.date_range(start="2020-01-01", periods=48, freq="ME")

starting_customers = 1000
subscription_price = 50
base_churn_rate = 0.05

data = []
active_customers = starting_customers

for month in months:
    seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * month.month / 12)
    new_customers = int(np.random.normal(120, 15) * seasonal_factor)
    churn_rate = base_churn_rate + np.random.normal(0, 0.005)
    churn_rate = max(churn_rate, 0.01)

    churned_customers = int(active_customers * churn_rate)
    active_customers = active_customers + new_customers - churned_customers
    mrr = active_customers * subscription_price

    data.append([month, active_customers, mrr])

df = pd.DataFrame(data, columns=["Month", "Active_Customers", "MRR"])

last_customers = df["Active_Customers"].iloc[-1]

future_months = 12
future_dates = pd.date_range(start=df["Month"].iloc[-1], periods=future_months + 1, freq="ME")[1:]

scenarios = {}

# Base case
customers = last_customers
base_projection = []

for _ in range(future_months):
    new = 120
    churn = customers * 0.05
    customers = customers + new - churn
    base_projection.append(customers * 50)

scenarios["Base"] = base_projection

# High Growth (+15% new customers)
customers = last_customers
high_growth = []

for _ in range(future_months):
    new = 120 * 1.15
    churn = customers * 0.05
    customers = customers + new - churn
    high_growth.append(customers * 50)

scenarios["High Growth"] = high_growth

# Churn Shock (+3% churn)
customers = last_customers
churn_shock = []

for _ in range(future_months):
    new = 120
    churn = customers * 0.08
    customers = customers + new - churn
    churn_shock.append(customers * 50)

scenarios["Churn Shock"] = churn_shock

# Pricing Increase (+8%)
customers = last_customers
pricing_increase = []

for _ in range(future_months):
    new = 120
    churn = customers * 0.05
    customers = customers + new - churn
    pricing_increase.append(customers * 50 * 1.08)

scenarios["Pricing Increase"] = pricing_increase

plt.figure(figsize=(10, 5))

for name, values in scenarios.items():
    plt.plot(future_dates, values, label=name)

plt.title("Revenue Scenario Analysis (Next 12 Months)")
plt.xlabel("Month")
plt.ylabel("Projected MRR")
plt.legend()
plt.tight_layout()
plt.show()

for name, values in scenarios.items():
    total_revenue = sum(values)
    print(f"{name} - Total 12M Revenue: {round(total_revenue, 2)}")

summary = []

for name, values in scenarios.items():
    total_revenue = sum(values)
    summary.append([name, total_revenue])

summary_df = pd.DataFrame(summary, columns=["Scenario", "Total_12M_Revenue"])

base_revenue = summary_df.loc[summary_df["Scenario"] == "Base", "Total_12M_Revenue"].values[0]

summary_df["%_Difference_vs_Base"] = (
    (summary_df["Total_12M_Revenue"] - base_revenue) / base_revenue
) * 100

print(summary_df)
