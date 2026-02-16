# SaaS Revenue Forecast & Scenario Analytics Dashboard

## Overview

An interactive SaaS revenue forecasting and scenario modeling dashboard built using Python and Streamlit.

This project simulates how changes in customer acquisition, churn, and pricing impact projected 12-month recurring revenue. It translates quantitative modeling into executive-level strategic insights.



## Business Problem

SaaS businesses rely on predictable recurring revenue.
Small shifts in churn, acquisition velocity, or pricing strategy can materially impact long-term financial performance.

This dashboard answers:

* How sensitive is revenue to churn shocks?
* What upside exists from growth acceleration?
* What is the impact of pricing adjustments?
* What is total revenue exposure under stress scenarios?



## Key Features

* Historical revenue simulation
* Time-series projection modeling
* 12-month forward revenue forecast
* Interactive scenario controls:

  * Growth multiplier
  * Churn rate adjustment
  * Pricing multiplier
* Revenue sensitivity ranking
* Revenue volatility quantification
* Automated executive insight generation



## Modeling Framework

Revenue is modeled as:

Revenue = Active Customers × Subscription Price

Customer base evolves monthly based on:

* New customer acquisition
* Churn rate
* Seasonal variation

Scenario projections dynamically adjust growth, churn, and pricing to simulate alternative business conditions.



## Scenario Results (Example Output)

* Churn shock: ~ −14.7% revenue vs base case
* Pricing increase: ~ +8% revenue vs base case
* Revenue volatility range: > $300K across stress scenarios
* Most sensitive lever: Churn rate

These results indicate revenue downside risk is driven primarily by churn acceleration rather than acquisition slowdown.



## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* Plotly
* Streamlit



## Project Structure

```
src/
    dashboard.py
    data_generation.py
    forecasting_model.py
    scenario_simulation.py

requirements.txt
README.md
```



## Run Locally

Install dependencies:

```
pip install -r requirements.txt
```

Launch dashboard:

```
streamlit run src/dashboard.py
```



## Strategic Value

This project demonstrates:

* Time-series forecasting
* Revenue sensitivity modeling
* Scenario stress testing
* Business risk quantification
* Executive-level analytics communication

It bridges technical modeling with strategic business decision-making.

