import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from financelib import calculations as calc
from financelib import data as fdata
from financelib import style

st.set_page_config(page_title="Projections · Finance Dashboard", page_icon="🔮", layout="wide")
style.inject()

accounts = fdata.load_accounts()
goals = fdata.load_goals()
contributions = fdata.load_contributions()

total = calc.total_balance(accounts)
recent_average = calc.average_monthly_contribution(contributions, months=3)

st.title("🔮 Projections")
st.caption("Scenario planning, not predictions. Change the assumptions and see how the trajectory moves.")

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        monthly = st.number_input(
            "Monthly contribution (£)",
            min_value=0.0,
            value=float(round(recent_average / 10) * 10) if recent_average else 1000.0,
            step=50.0,
        )
    with c2:
        years = st.slider("Years", 1, 30, 15)
    with c3:
        inflation = st.number_input("Inflation assumption (%/yr)", min_value=0.0, max_value=10.0, value=2.5, step=0.5)

    low, mid, high = st.columns(3)
    with low:
        low_rate = st.number_input("Low return (%/yr)", min_value=-10.0, max_value=20.0, value=2.0, step=0.5)
    with mid:
        mid_rate = st.number_input("Mid return (%/yr)", min_value=-10.0, max_value=20.0, value=5.0, step=0.5)
    with high:
        high_rate = st.number_input("High return (%/yr)", min_value=-10.0, max_value=20.0, value=8.0, step=0.5)

st.write("")

# ------------------------------------------------------------------
# Scenario chart
# ------------------------------------------------------------------

scenario_values = {
    "Low": calc.project(total, monthly, low_rate, years),
    "Mid": calc.project(total, monthly, mid_rate, years),
    "High": calc.project(total, monthly, high_rate, years),
}

with st.container(border=True):
    st.markdown("##### Net Worth Projection")
    fig = go.Figure()
    for name, values, dash, width in [
        ("Low", scenario_values["Low"], "dot", 2),
        ("High", scenario_values["High"], "dot", 2),
        ("Mid", scenario_values["Mid"], "solid", 3),
    ]:
        rate = {"Low": low_rate, "Mid": mid_rate, "High": high_rate}[name]
        fig.add_trace(go.Scatter(
            x=list(range(years + 1)),
            y=values,
            mode="lines",
            name=f"{name} · {rate:g}%",
            line=dict(
                color={"Low": "#64748B", "Mid": "#22C55E", "High": "#38BDF8"}[name],
                width=width,
                dash=dash,
            ),
            hovertemplate="Year %{x}<br><b>£%{y:,.0f}</b><extra>%{fullData.name}</extra>",
        ))

    style.plotly_layout(fig, height=420)
    fig.update_xaxes(title="Years from today")
    fig.update_yaxes(title="Net worth", tickprefix="£", separatethousands=True)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

# ------------------------------------------------------------------
# Scenario summary
# ------------------------------------------------------------------

summary_rows = []
for name, rate in [("Low", low_rate), ("Mid", mid_rate), ("High", high_rate)]:
    breakdown = calc.projection_breakdown(total, monthly, rate, years)
    summary_rows.append({
        "Scenario": name,
        "Return": f"{rate:g}%",
        "Final value": f"£{breakdown['final_value']:,.0f}",
        "Your contributions": f"£{breakdown['contributions']:,.0f}",
        "Growth": f"£{breakdown['growth']:,.0f}",
    })

with st.container(border=True):
    st.markdown("##### What drives the result?")
    st.dataframe(pd.DataFrame(summary_rows).set_index("Scenario"), width="stretch")
    st.caption(
        f"At £{monthly:,.0f}/month, your own contributions over {years} years would total £{monthly * 12 * years:,.0f}. "
        "The rest of the projected value is growth under the selected scenario."
    )

# Inflation-adjusted mid case
mid_nominal = scenario_values["Mid"][-1]
mid_real = mid_nominal / ((1 + inflation / 100) ** years)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(f"Mid-case after {years} years", f"£{mid_nominal:,.0f}")
with m2:
    st.metric("In today's money", f"£{mid_real:,.0f}")
with m3:
    st.metric("Starting net worth", f"£{total:,.0f}")

st.write("")

# ------------------------------------------------------------------
# Goal timing
# ------------------------------------------------------------------

accumulation_goals = [g for g in goals if g.get("kind") == "accumulation"]
if accumulation_goals:
    with st.container(border=True):
        st.markdown("##### Time to reach a goal")
        goal = st.selectbox(
            "Goal",
            accumulation_goals,
            format_func=lambda g: g["name"],
        )
        rate_choice = st.radio("Scenario", ["Low", "Mid", "High"], horizontal=True, index=1)
        rate = {"Low": low_rate, "Mid": mid_rate, "High": high_rate}[rate_choice]
        accounts_by_id = {a["id"]: a for a in accounts}
        current = sum(
            accounts_by_id[i]["balance"]
            for i in goal.get("accounts", [])
            if i in accounts_by_id
        )
        months = calc.months_to_target(current, monthly, rate, goal["target"])
        if months == 0:
            st.success(f"{goal['name']} is already reached.")
        elif months is None:
            st.warning("This target is not reached within 50 years using these assumptions.")
        else:
            y, m = divmod(months, 12)
            parts = []
            if y:
                parts.append(f"{y}y")
            if m:
                parts.append(f"{m}m")
            st.metric("Estimated time", " ".join(parts) or "Now")
            st.caption(
                f"Starting from £{current:,.0f}, contributing £{monthly:,.0f}/month at {rate:g}% annual growth."
            )
