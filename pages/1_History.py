from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from financelib import calculations as calc
from financelib import data as fdata
from financelib import style

st.set_page_config(page_title="History · Finance Dashboard", page_icon="📈", layout="wide")
style.inject()

accounts = fdata.load_accounts()
history = fdata.load_history()
contributions = fdata.load_contributions()

st.title("📈 History")
st.caption("Your financial timeline — snapshots, monthly movement and contribution tracking.")

# ------------------------------------------------------------------
# Capture data
# ------------------------------------------------------------------

snap_col, contrib_col = st.columns([1.1, 0.9], gap="large")

with snap_col:
    with st.container(border=True):
        st.markdown("##### Record a monthly snapshot")
        st.caption("Enter your balances at the point you want this month represented. Saving updates current balances too.")
        with st.form("snapshot_form"):
            month_str = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"))
            balances = {}
            cols = st.columns(2)
            for i, account in enumerate(accounts):
                with cols[i % 2]:
                    balances[account["id"]] = st.number_input(
                        account["name"],
                        min_value=0.0,
                        value=float(account["balance"]),
                        step=10.0,
                    )
            preview_total = sum(balances.values())
            st.metric("Snapshot net worth", f"£{preview_total:,.0f}")
            if st.form_submit_button("Save snapshot", use_container_width=True):
                if len(month_str) != 7 or month_str[4] != "-":
                    st.error("Use YYYY-MM, for example 2026-09.")
                else:
                    fdata.add_snapshot(month_str, balances)
                    updated_accounts = [
                        {**a, "balance": balances[a["id"]]} for a in accounts
                    ]
                    fdata.save_accounts(updated_accounts)
                    st.success(f"Saved {month_str} snapshot.")
                    st.rerun()

with contrib_col:
    with st.container(border=True):
        st.markdown("##### Log a contribution")
        st.caption("Keeping contributions separate lets the app distinguish saving from investment growth.")
        with st.form("contribution_form"):
            c_date = st.date_input("Date", value=date.today())
            c_account = st.selectbox(
                "Account",
                [a["id"] for a in accounts],
                format_func=lambda i: next(a["name"] for a in accounts if a["id"] == i),
            )
            c_amount = st.number_input("Amount (£)", min_value=0.0, step=25.0)
            c_note = st.text_input("Note", placeholder="Salary, monthly investment, LISA, etc.")
            if st.form_submit_button("Log contribution", use_container_width=True):
                if c_amount <= 0:
                    st.error("Enter an amount greater than £0.")
                else:
                    fdata.log_contribution(c_date.isoformat(), c_account, c_amount, c_note)
                    st.success("Contribution logged.")
                    st.rerun()

st.write("")

# ------------------------------------------------------------------
# Trend analysis
# ------------------------------------------------------------------

with st.container(border=True):
    st.markdown("##### Net Worth Trend")
    if len(history) < 2:
        st.info("Save at least two snapshots to build a trend.")
    else:
        months = [h["month"] for h in sorted(history, key=lambda x: x["month"])]
        selected_months = st.select_slider(
            "Visible range",
            options=months,
            value=(months[max(0, len(months) - 12)], months[-1]),
            label_visibility="collapsed",
        )
        start_i = months.index(selected_months[0])
        end_i = months.index(selected_months[1]) + 1
        shown_history = sorted(history, key=lambda x: x["month"])[start_i:end_i]

        account_filter = st.multiselect(
            "Accounts to show",
            [a["id"] for a in accounts],
            default=[a["id"] for a in accounts],
            format_func=lambda i: next(a["name"] for a in accounts if a["id"] == i),
        )

        fig = go.Figure()
        palette = ["#22C55E", "#38BDF8", "#A78BFA", "#F59E0B", "#F472B6", "#94A3B8"]
        for idx, account_id in enumerate(account_filter):
            fig.add_trace(go.Scatter(
                x=[h["month"] for h in shown_history],
                y=[h.get("balances", {}).get(account_id, 0) for h in shown_history],
                mode="lines+markers",
                name=next((a["name"] for a in accounts if a["id"] == account_id), account_id),
                line=dict(color=palette[idx % len(palette)], width=2.5),
                marker=dict(size=5),
                hovertemplate="%{x}<br>£%{y:,.0f}<extra>%{fullData.name}</extra>",
            ))
        fig.add_trace(go.Scatter(
            x=[h["month"] for h in shown_history],
            y=[calc.snapshot_total(h) for h in shown_history],
            mode="lines",
            name="Total net worth",
            line=dict(color="#F8FAFC", width=3, dash="dot"),
            hovertemplate="%{x}<br><b>£%{y:,.0f}</b><extra>Total</extra>",
        ))
        style.plotly_layout(fig, height=410, showlegend=True)
        fig.update_yaxes(tickprefix="£", separatethousands=True)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

# ------------------------------------------------------------------
# Monthly table
# ------------------------------------------------------------------

with st.container(border=True):
    st.markdown("##### Monthly Snapshot Table")
    if history:
        rows = []
        for h in sorted(history, key=lambda x: x["month"], reverse=True):
            rows.append({
                "Month": h["month"],
                "Net worth": calc.snapshot_total(h),
            })
        table = pd.DataFrame(rows)
        table["Change"] = table["Net worth"].diff(periods=-1)
        table["Net worth"] = table["Net worth"].map(lambda x: f"£{x:,.0f}")
        table["Change"] = table["Change"].map(lambda x: "—" if pd.isna(x) else f"{'+' if x >= 0 else '-'}£{abs(x):,.0f}")
        st.dataframe(table.set_index("Month"), width="stretch")
    else:
        st.info("No snapshots yet.")

# ------------------------------------------------------------------
# Contribution analysis
# ------------------------------------------------------------------

with st.container(border=True):
    st.markdown("##### Contributions")
    if not contributions:
        st.info("No contributions logged yet. Start logging them and this page will build your saving history.")
    else:
        contributions_df = pd.DataFrame(contributions)
        contributions_df["Account"] = contributions_df["account_id"].map(
            {a["id"]: a["name"] for a in accounts}
        )
        contributions_df["Amount"] = contributions_df["amount"].map(lambda x: f"£{x:,.0f}")
        contributions_df = contributions_df.rename(columns={"date": "Date", "note": "Note"})
        st.dataframe(
            contributions_df[["Date", "Account", "Amount", "Note"]].sort_values("Date", ascending=False),
            width="stretch",
            hide_index=True,
        )
