import streamlit as st

from financelib import calculations as calc
from financelib import data as fdata
from financelib import style

st.set_page_config(page_title="Goals · Finance Dashboard", page_icon="🎯", layout="wide")
style.inject()

accounts = fdata.load_accounts()
goals = fdata.load_goals()
contributions = fdata.load_contributions()
accounts_by_id = {a["id"]: a for a in accounts}

st.title("🎯 Goals")
st.caption("Track the things your money is actually meant to accomplish.")

# ------------------------------------------------------------------
# Goal cards
# ------------------------------------------------------------------

if not goals:
    st.info("No goals configured yet. Add them to data/goals.json for now; a proper in-app goal editor can come later.")
else:
    goal_cols = st.columns(len(goals))
    for col, goal in zip(goal_cols, goals):
        with col:
            with st.container(border=True):
                icon = "🏠" if goal["id"] == "house_deposit" else "🎯"
                st.markdown(f"##### {icon} {goal['name']}")

                if goal["kind"] == "accumulation":
                    current = sum(
                        accounts_by_id[i]["balance"]
                        for i in goal.get("accounts", [])
                        if i in accounts_by_id
                    )
                    target = float(goal.get("target", 0))
                    progress = min(current / target, 1) if target else 0
                    remaining = max(target - current, 0)
                    st.progress(progress)
                    st.metric("Progress", f"{progress:.0%}")
                    c1, c2 = st.columns(2)
                    c1.metric("Current", f"£{current:,.0f}")
                    c2.metric("Target", f"£{target:,.0f}")
                    st.caption(f"£{remaining:,.0f} remaining")
                    funded_by = ", ".join(
                        accounts_by_id[i]["name"] for i in goal.get("accounts", []) if i in accounts_by_id
                    )
                    st.caption(f"Funded by: {funded_by}")
                else:
                    target = float(goal.get("target", 0))
                    spent = float(goal.get("spent", 0))
                    progress = min(spent / target, 1) if target else 0
                    st.progress(progress)
                    c1, c2 = st.columns(2)
                    c1.metric("Used", f"£{spent:,.0f}")
                    c2.metric("Budget", f"£{target:,.0f}")
                    st.caption(f"£{max(target - spent, 0):,.0f} remaining")

                if goal.get("note"):
                    st.caption(goal["note"])

                if goal["kind"] == "budget":
                    new_spent = st.number_input(
                        "Update spent",
                        min_value=0.0,
                        value=spent,
                        step=25.0,
                        key=f"spent_{goal['id']}",
                    )
                    if st.button("Save", key=f"save_{goal['id']}", use_container_width=True):
                        fdata.update_goal_field(goal["id"], "spent", new_spent)
                        st.success("Updated.")
                        st.rerun()

st.write("")

# ------------------------------------------------------------------
# UK tax wrappers
# ------------------------------------------------------------------

lisa_account = next((a for a in accounts if a.get("lisa")), None)
if lisa_account:
    with st.container(border=True):
        st.markdown("##### 🏦 LISA Bonus Tracker")
        status = calc.lisa_bonus_status(contributions, lisa_account["id"])
        used_pct = min(status["contributed"] / status["limit"], 1) if status["limit"] else 0

        a, b, c = st.columns(3)
        a.metric(f"Paid in · {status['tax_year']}", f"£{status['contributed']:,.0f}")
        b.metric("Bonus earned", f"£{status['bonus_earned']:,.0f}")
        c.metric("Bonus still available", f"£{status['bonus_available']:,.0f}")
        st.progress(used_pct)
        st.caption(
            f"£{status['remaining_allowance']:,.0f} of the £{status['limit']:,.0f} annual LISA contribution limit remains."
        )
        st.caption("Current GOV.UK rules: the LISA bonus is 25% of contributions, up to £1,000 per tax year.")

isa_account_ids = [a["id"] for a in accounts if a.get("type") != "pension"]
if isa_account_ids:
    with st.container(border=True):
        st.markdown("##### 📋 ISA Allowance")
        status = calc.isa_allowance_status(contributions, isa_account_ids)
        used_pct = min(status["used"] / status["allowance"], 1) if status["allowance"] else 0
        c1, c2, c3 = st.columns(3)
        c1.metric("Used", f"£{status['used']:,.0f}")
        c2.metric("Total allowance", f"£{status['allowance']:,.0f}")
        c3.metric("Remaining", f"£{status['remaining']:,.0f}")
        st.progress(used_pct)
        st.caption(
            f"2026/27 overall ISA subscription limit: £20,000. From 6 April 2027, the annual Cash ISA limit for under-65s is scheduled to be £12,000 within the £20,000 overall ISA limit."
        )
