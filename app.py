import json
from datetime import date, datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from financelib import calculations as calc
from financelib import data as fdata
from financelib import style

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)
style.inject()

accounts_meta = fdata.load_accounts_full()
accounts = accounts_meta.get("accounts", [])
history = fdata.load_history()
goals = fdata.load_goals()
contributions = fdata.load_contributions()

if not accounts:
    st.error("No accounts found in data/accounts.json.")
    st.stop()


def account_name(account_id):
    return next((a["name"] for a in accounts if a["id"] == account_id), account_id)


def save_current_balances(month, balances):
    fdata.add_snapshot(month, balances)
    updated = []
    for account in accounts:
        updated.append({**account, "balance": balances[account["id"]]})
    fdata.save_accounts(updated)


def delta_text(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}£{abs(value):,.0f} vs previous snapshot"


# ------------------------------------------------------------------
# Header + quick update
# ------------------------------------------------------------------

header_left, header_right = st.columns([7, 1])
with header_left:
    st.title("💰 Finance Dashboard")
    st.caption("Your financial position, history, goals and trajectory in one place.")
with header_right:
    with st.popover("✏️ Update", use_container_width=True):
        st.markdown("**Update balances**")
        st.caption("Saving also records a monthly snapshot, so the history chart keeps building.")
        with st.form("quick_update"):
            snapshot_month = st.text_input(
                "Snapshot month (YYYY-MM)",
                value=date.today().strftime("%Y-%m"),
            )
            new_balances = {}
            for account in accounts:
                new_balances[account["id"]] = st.number_input(
                    account["name"],
                    min_value=0.0,
                    value=float(account["balance"]),
                    step=10.0,
                )
            if st.form_submit_button("Save balances", use_container_width=True):
                if len(snapshot_month) != 7 or snapshot_month[4] != "-":
                    st.error("Use YYYY-MM, for example 2026-09.")
                else:
                    try:
                        datetime.strptime(snapshot_month, "%Y-%m")
                    except ValueError:
                        st.error("Enter a real month in YYYY-MM format, for example 2026-09.")
                    else:
                        save_current_balances(snapshot_month, new_balances)
                        st.success("Balances and monthly snapshot saved.")
                        st.rerun()

# ------------------------------------------------------------------
# Current position
# ------------------------------------------------------------------

total = calc.total_balance(accounts)
previous_change = calc.month_change(history)
investment_total = calc.balance_by_type(accounts, "investment")
cash_total = calc.balance_by_type(accounts, "cash")
pension_total = calc.balance_by_type(accounts, "pension")
allocated = calc.allocation(accounts)

style.hero(
    f"£{total:,.0f}",
    delta_text(previous_change) if previous_change is not None else None,
    positive=(previous_change is None or previous_change >= 0),
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Investments", f"£{investment_total:,.0f}")
    st.caption(f"{investment_total / total:.0%} of net worth" if total else "0% of net worth")
with k2:
    st.metric("Cash", f"£{cash_total:,.0f}")
    st.caption(f"{cash_total / total:.0%} of net worth" if total else "0% of net worth")
with k3:
    st.metric("Pension", f"£{pension_total:,.0f}")
    st.caption(f"{pension_total / total:.0%} of net worth" if total else "0% of net worth")
with k4:
    latest_month = max((h["month"] for h in history), default="—")
    st.metric("Latest snapshot", latest_month)
    st.caption("Monthly history")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# Accounts row
# ------------------------------------------------------------------

st.markdown('<div class="section-title">Accounts</div>', unsafe_allow_html=True)
account_cols = st.columns(len(accounts))
for col, account in zip(account_cols, allocated):
    with col:
        style.account_card(
            style.TYPE_ICONS.get(account.get("type"), "💼"),
            account["name"],
            float(account["balance"]),
            float(account["percentage"]),
        )

st.write("")

# ------------------------------------------------------------------
# Main analytics row
# ------------------------------------------------------------------

left, right = st.columns([1.45, 1], gap="large")

with left:
    with st.container(border=True):
        st.markdown("##### Net Worth Over Time")
        period_options = {"3M": 3, "6M": 6, "1Y": 12, "3Y": 36, "All": None}
        period = st.radio("Period", list(period_options), horizontal=True, label_visibility="collapsed", index=4)

        totals = calc.history_totals(history)
        if len(totals) < 2:
            st.info("Save another monthly snapshot to start building your trend line.")
        else:
            shown = totals[-period_options[period]:] if period_options[period] else totals
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[x["month"] for x in shown],
                y=[x["net_worth"] for x in shown],
                mode="lines+markers",
                line=dict(color="#22C55E", width=3, shape="spline"),
                marker=dict(size=7, color="#22C55E"),
                fill="tozeroy",
                fillcolor="rgba(34,197,94,0.10)",
                hovertemplate="%{x}<br><b>£%{y:,.0f}</b><extra></extra>",
            ))
            style.plotly_layout(fig, height=360, showlegend=False)
            fig.update_yaxes(tickprefix="£", separatethousands=True)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

            first = shown[0]["net_worth"]
            last = shown[-1]["net_worth"]
            period_change = last - first
            st.caption(
                f"{period} change: **{'+' if period_change >= 0 else '-'}£{abs(period_change):,.0f}** · "
                f"{len(shown)} snapshots"
            )

with right:
    with st.container(border=True):
        st.markdown("##### Allocation")
        fig = go.Figure(go.Pie(
            labels=[a["name"] for a in accounts],
            values=[a["balance"] for a in accounts],
            hole=0.66,
            sort=False,
            textinfo="percent",
            textposition="outside",
            marker=dict(
                colors=[style.TYPE_COLORS.get(a.get("type"), "#94A3B8") for a in accounts],
                line=dict(color="#121820", width=3),
            ),
            hovertemplate="<b>%{label}</b><br>£%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig.add_annotation(
            text=f"<b>£{total:,.0f}</b><br><span style='font-size:11px'>net worth</span>",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=20, color="#F8FAFC"),
        )
        style.plotly_layout(fig, height=360, showlegend=True)
        fig.update_layout(legend=dict(orientation="v", y=0.5, x=1.02, xanchor="left"))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

st.write("")

# ------------------------------------------------------------------
# Monthly movement
# ------------------------------------------------------------------

with st.container(border=True):
    st.markdown("##### Monthly Movement")
    if len(history) < 2:
        st.info("Your monthly movement will appear here once you have at least two snapshots.")
    else:
        ordered = sorted(history, key=lambda h: h["month"])
        rows = []
        for i in range(1, len(ordered)):
            prev = calc.snapshot_total(ordered[i - 1])
            current = calc.snapshot_total(ordered[i])
            month = ordered[i]["month"]
            year, mon = map(int, month.split("-"))
            contributions_month = calc.monthly_contribution_total(contributions, year, mon)
            rows.append({
                "Month": month,
                "Net worth": current,
                "Change": current - prev,
                "Contributions": contributions_month,
            })

        movement_df = pd.DataFrame(rows).tail(12)
        c1, c2 = st.columns([1.25, 1])
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=movement_df["Month"],
                y=movement_df["Change"],
                marker_color=["#22C55E" if x >= 0 else "#F87171" for x in movement_df["Change"]],
                hovertemplate="%{x}<br><b>£%{y:+,.0f}</b><extra></extra>",
            ))
            style.plotly_layout(fig, height=280, showlegend=False)
            fig.update_yaxes(tickprefix="£", separatethousands=True)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        with c2:
            st.dataframe(
                movement_df.iloc[::-1].assign(
                    **{
                        "Net worth": movement_df["Net worth"].map(lambda x: f"£{x:,.0f}"),
                        "Change": movement_df["Change"].map(lambda x: f"{'+' if x >= 0 else '-'}£{abs(x):,.0f}"),
                        "Contributions": movement_df["Contributions"].map(lambda x: f"£{x:,.0f}"),
                    }
                ).set_index("Month")[['Net worth', 'Change', 'Contributions']],
                width="stretch",
                hide_index=False,
            )
            st.caption("Contributions are only shown when you log them on the History page.")

st.write("")

# ------------------------------------------------------------------
# Goals + useful callouts
# ------------------------------------------------------------------

st.markdown('<div class="section-title">Goals & Next Actions</div>', unsafe_allow_html=True)
if goals:
    goal_cols = st.columns(len(goals))
    for col, goal in zip(goal_cols, goals):
        with col:
            with st.container(border=True):
                icon = "🏠" if goal["id"] == "house_deposit" else "🎯"
                st.markdown(f"##### {icon} {goal['name']}")
                if goal["kind"] == "accumulation":
                    current = sum(a["balance"] for a in accounts if a["id"] in goal.get("accounts", []))
                    target = float(goal.get("target", 0))
                    progress = min(current / target, 1) if target else 0
                    st.progress(progress)
                    st.write(f"**£{current:,.0f} / £{target:,.0f}** · {progress:.0%}")
                    st.caption(f"£{max(target - current, 0):,.0f} remaining")
                else:
                    spent = float(goal.get("spent", 0))
                    target = float(goal.get("target", 0))
                    progress = min(spent / target, 1) if target else 0
                    st.progress(progress)
                    st.write(f"**£{spent:,.0f} / £{target:,.0f} used** · {progress:.0%}")
                    st.caption(f"£{max(target - spent, 0):,.0f} remaining")
else:
    st.info("No goals configured yet.")

last_update = accounts_meta.get("last_updated") or "not recorded"
st.caption(f"Balances last updated: {last_update} · Historical snapshots are stored separately from current balances.")
