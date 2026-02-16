import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="SaaS Revenue Dashboard", layout="wide")

st.title("SaaS Revenue Forecast & Scenario Dashboard")

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
    churn_rate = max(base_churn_rate + np.random.normal(0, 0.005), 0.01)
    churned_customers = int(active_customers * churn_rate)
    active_customers = active_customers + new_customers - churned_customers
    mrr = active_customers * subscription_price
    data.append([month, active_customers, mrr])

df = pd.DataFrame(data, columns=["Month", "Active_Customers", "MRR"])

col1, col2, col3 = st.columns(3)

col1.metric("Latest MRR", f"${df['MRR'].iloc[-1]:,.0f}")
col2.metric("Active Customers", f"{df['Active_Customers'].iloc[-1]:,.0f}")
col3.metric("Average Monthly Growth %",
            f"{df['MRR'].pct_change().mean()*100:.2f}%")

st.subheader("Historical Revenue Trend")

fig_hist = px.line(df, x="Month", y="MRR",
                   title="Monthly Recurring Revenue")
fig_hist.update_layout(height=500)
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Scenario Controls")

growth_multiplier = st.slider("New Customer Growth Multiplier", 0.5, 1.5, 1.0)
churn_rate_input = st.slider("Churn Rate (%)", 1, 15, 5) / 100
price_multiplier = st.slider("Pricing Multiplier", 0.8, 1.2, 1.0)

last_customers = df["Active_Customers"].iloc[-1]
future_months = 12
future_dates = pd.date_range(
    start=df["Month"].iloc[-1],
    periods=future_months + 1,
    freq="ME"
)[1:]

def simulate_scenario(growth_mult, churn_rate, price_mult):
    customers = last_customers
    values = []

    for _ in range(future_months):
        new = 120 * growth_mult
        churn = customers * churn_rate
        customers = customers + new - churn
        values.append(customers * 50 * price_mult)

    return values

base_proj = simulate_scenario(1.0, 0.05, 1.0)
high_growth_proj = simulate_scenario(1.2, 0.05, 1.0)
churn_shock_proj = simulate_scenario(1.0, 0.08, 1.0)
pricing_proj = simulate_scenario(1.0, 0.05, 1.08)

scenario_df = pd.DataFrame({
    "Month": future_dates,
    "Base": base_proj,
    "High Growth": high_growth_proj,
    "Churn Shock": churn_shock_proj,
    "Pricing Increase": pricing_proj
})

st.subheader("Scenario Comparison (Next 12 Months)")

fig_compare = px.line(
    scenario_df,
    x="Month",
    y=["Base", "High Growth", "Churn Shock", "Pricing Increase"],
    title="Revenue Scenario Comparison"
)

fig_compare.update_layout(height=500)
st.plotly_chart(fig_compare, use_container_width=True)

totals = {
    "Base": sum(base_proj),
    "High Growth": sum(high_growth_proj),
    "Churn Shock": sum(churn_shock_proj),
    "Pricing Increase": sum(pricing_proj)
}

summary_df = pd.DataFrame({
    "Scenario": totals.keys(),
    "Total_12M_Revenue": totals.values()
})

base_value = totals["Base"]

summary_df["% Difference vs Base"] = (
    (summary_df["Total_12M_Revenue"] - base_value) / base_value
) * 100

st.subheader("12-Month Revenue Summary")
st.dataframe(summary_df)

fig_bar = px.bar(
    summary_df,
    x="Scenario",
    y="Total_12M_Revenue",
    title="Total 12-Month Revenue by Scenario",
    text_auto=".2s"
)

fig_bar.update_layout(height=400)
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Revenue Sensitivity Analysis")

summary_df["Abs_%_Impact"] = summary_df["% Difference vs Base"].abs()
ranked = summary_df.sort_values("Abs_%_Impact", ascending=False)

st.dataframe(ranked[["Scenario", "% Difference vs Base"]])

max_rev = summary_df["Total_12M_Revenue"].max()
min_rev = summary_df["Total_12M_Revenue"].min()
volatility_range = max_rev - min_rev

st.metric("Revenue Volatility Range (Best vs Worst Case)",
          f"${volatility_range:,.0f}")

most_sensitive = ranked.iloc[0]["Scenario"]

st.subheader("Executive Decision Insight")

st.markdown(f"""
**Key Finding:**  
Revenue is most sensitive to changes in **{most_sensitive}**.

Even modest shifts in this driver create disproportionate impact on projected revenue.
Strategic focus should prioritize stabilizing this lever before pursuing aggressive growth initiatives.
""")
