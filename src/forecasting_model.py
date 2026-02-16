import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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

    data.append([month, mrr])

df = pd.DataFrame(data, columns=["Month", "MRR"])

df["Time_Index"] = np.arange(len(df))
df["Month_Num"] = df["Month"].dt.month

df = pd.get_dummies(df, columns=["Month_Num"], drop_first=True)

X = df.drop(columns=["Month", "MRR"])
y = df["MRR"]

model = LinearRegression()
model.fit(X, y)

predictions = model.predict(X)

rmse = np.sqrt(mean_squared_error(y, predictions))
print("RMSE:", round(rmse, 2))

future_periods = 12
last_time_index = df["Time_Index"].max()

future_dates = pd.date_range(
    start=df["Month"].iloc[-1],
    periods=future_periods + 1,
    freq="ME"
)[1:]

future_df = pd.DataFrame({
    "Month": future_dates,
    "Time_Index": np.arange(last_time_index + 1, last_time_index + 1 + future_periods)
})

future_df["Month_Num"] = future_df["Month"].dt.month
future_df = pd.get_dummies(future_df, columns=["Month_Num"], drop_first=True)

for col in X.columns:
    if col not in future_df.columns:
        future_df[col] = 0

future_df = future_df[X.columns]

future_predictions = model.predict(future_df)

plt.figure(figsize=(10, 5))
plt.plot(df["Month"], y, label="Actual")
plt.plot(df["Month"], predictions, label="Fitted (Trend + Seasonality)")
plt.plot(future_dates, future_predictions, label="Forecast", linestyle="dashed")

plt.title("Revenue Forecast (Trend + Seasonality Model)")
plt.xlabel("Month")
plt.ylabel("MRR")
plt.legend()
plt.tight_layout()
plt.show()
