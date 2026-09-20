import json
import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💰",
    layout="wide"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

with open("data/balances.json") as file:
    data = json.load(file)

accounts = data["accounts"]


# ---------------------------------------------------------
# Calculations
# ---------------------------------------------------------

total = sum(account["balance"] for account in accounts)

for account in accounts:
    account["percentage"] = (
        account["balance"] / total * 100
        if total > 0
        else 0
    )


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("💰 Finance Dashboard")
st.caption("A personal overview of my financial position and trajectory.")


# ---------------------------------------------------------
# Top-level metrics
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Net Worth",
        value=f"£{total:,.0f}"
    )

with col2:
    investment_total = sum(
        account["balance"]
        for account in accounts
        if account.get("type") == "investment"
    )

    st.metric(
        label="Investments",
        value=f"£{investment_total:,.0f}"
    )

with col3:
    cash_total = sum(
        account["balance"]
        for account in accounts
        if account.get("type") == "cash"
    )

    st.metric(
        label="Cash",
        value=f"£{cash_total:,.0f}"
    )


st.divider()


# ---------------------------------------------------------
# Account breakdown
# ---------------------------------------------------------

st.subheader("Accounts")

columns = st.columns(len(accounts))

for i, account in enumerate(accounts):

    with columns[i]:

        st.metric(
            label=account["name"],
            value=f"£{account['balance']:,.0f}"
        )

        st.caption(
            f"{account['percentage']:.0f}% of net worth"
        )


st.divider()


# ---------------------------------------------------------
# Allocation chart
# ---------------------------------------------------------

st.subheader("Portfolio Allocation")

chart_data = pd.DataFrame(
    {
        "Account": [
            account["name"]
            for account in accounts
        ],
        "Balance": [
            account["balance"]
            for account in accounts
        ]
    }
)

st.bar_chart(
    chart_data,
    x="Account",
    y="Balance"
)

# ---------------------------------------------------------
# Financial projection
# ---------------------------------------------------------

st.subheader("Financial Projection")

projection_col1, projection_col2 = st.columns(2)

with projection_col1:

    monthly_contribution = st.number_input(
        "Monthly contribution (£)",
        min_value=0,
        value=1000,
        step=50
    )

with projection_col2:

    annual_growth = st.number_input(
        "Expected annual growth (%)",
        min_value=0.0,
        max_value=30.0,
        value=7.0,
        step=0.5
    )


years = list(range(0, 21))

projected_values = []

current_value = total

for year in years:

    if year == 0:
        projected_values.append(current_value)
        continue

    current_value = (
        current_value * (1 + annual_growth / 100)
        + monthly_contribution * 12
    )

    projected_values.append(current_value)


projection_data = pd.DataFrame(
    {
        "Year": years,
        "Projected Net Worth": projected_values
    }
)

st.line_chart(
    projection_data,
    x="Year",
    y="Projected Net Worth"
)

st.caption(
    f"After 20 years: approximately "
    f"£{projected_values[-1]:,.0f}"
)


st.divider()


# ---------------------------------------------------------
# Financial goals
# ---------------------------------------------------------

st.subheader("Financial Goals")

goal_col1, goal_col2 = st.columns(2)

with goal_col1:

    goal_name = st.text_input(
        "Goal",
        value="£100k Net Worth"
    )

with goal_col2:

    goal_target = st.number_input(
        "Target amount (£)",
        min_value=1,
        value=100000,
        step=5000
    )


goal_progress = min(total / goal_target, 1)

st.progress(goal_progress)

st.write(
    f"**£{total:,.0f} / £{goal_target:,.0f}** "
    f"({goal_progress * 100:.1f}%)"
)

remaining = max(goal_target - total, 0)

if remaining > 0:

    st.caption(
        f"£{remaining:,.0f} remaining to reach {goal_name}"
    )

else:

    st.success(
        f"🎉 You've reached {goal_name}!"
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Finance Dashboard • Built with Python + Streamlit"
)