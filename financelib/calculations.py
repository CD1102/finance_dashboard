"""Pure financial calculations.

No Streamlit and no file I/O live here. Keeping calculations separate makes the
logic easier to test now and easier to reuse when JSON is replaced by a database.
"""

from datetime import date


def total_balance(accounts):
    return sum(float(a.get("balance", 0)) for a in accounts)


def balance_by_type(accounts, type_name):
    return sum(float(a.get("balance", 0)) for a in accounts if a.get("type") == type_name)


def allocation(accounts):
    total = total_balance(accounts)
    return [
        {**a, "percentage": (float(a.get("balance", 0)) / total * 100) if total else 0}
        for a in accounts
    ]


def snapshot_total(snapshot):
    return sum(float(v) for v in snapshot.get("balances", {}).values())


def history_totals(history):
    return [
        {"month": h["month"], "net_worth": snapshot_total(h)}
        for h in sorted(history, key=lambda x: x["month"])
    ]


def latest_snapshot(history):
    return max(history, key=lambda x: x["month"]) if history else None


def previous_snapshot(history):
    ordered = sorted(history, key=lambda x: x["month"])
    return ordered[-2] if len(ordered) >= 2 else None


def month_change(history):
    ordered = sorted(history, key=lambda x: x["month"])
    if len(ordered) < 2:
        return None
    return snapshot_total(ordered[-1]) - snapshot_total(ordered[-2])


def change_between(history, start_month, end_month):
    lookup = {h["month"]: snapshot_total(h) for h in history}
    if start_month not in lookup or end_month not in lookup:
        return None
    return lookup[end_month] - lookup[start_month]


def account_changes_between(history, start_month, end_month):
    snapshots = {h["month"]: h for h in history}
    start = snapshots.get(start_month)
    end = snapshots.get(end_month)
    if not start or not end:
        return {}

    account_ids = set(start.get("balances", {})) | set(end.get("balances", {}))
    return {
        account_id: float(end.get("balances", {}).get(account_id, 0))
        - float(start.get("balances", {}).get(account_id, 0))
        for account_id in account_ids
    }


def contributions_in_range(contributions, account_id=None, start=None, end=None):
    total = 0.0
    for c in contributions:
        c_date = date.fromisoformat(c["date"])
        if account_id is not None and c.get("account_id") != account_id:
            continue
        if start is not None and c_date < start:
            continue
        if end is not None and c_date > end:
            continue
        total += float(c.get("amount", 0))
    return total


def monthly_contribution_total(contributions, year, month):
    total = 0.0
    for c in contributions:
        c_date = date.fromisoformat(c["date"])
        if c_date.year == year and c_date.month == month:
            total += float(c.get("amount", 0))
    return total


def current_tax_year(today=None):
    today = today or date.today()
    if today >= date(today.year, 4, 6):
        start = date(today.year, 4, 6)
        end = date(today.year + 1, 4, 5)
    else:
        start = date(today.year - 1, 4, 6)
        end = date(today.year, 4, 5)
    label = f"{start.year}/{str(end.year)[-2:]}"
    return label, start, end


LISA_ANNUAL_LIMIT = 4000
LISA_BONUS_RATE = 0.25
ISA_ANNUAL_ALLOWANCE = 20000


def lisa_bonus_status(contributions, lisa_account_id, today=None):
    label, start, end = current_tax_year(today)
    contributed = contributions_in_range(contributions, lisa_account_id, start, end)
    contributed_capped = min(contributed, LISA_ANNUAL_LIMIT)
    remaining_allowance = max(LISA_ANNUAL_LIMIT - contributed, 0)
    return {
        "tax_year": label,
        "contributed": contributed,
        "remaining_allowance": remaining_allowance,
        "bonus_earned": contributed_capped * LISA_BONUS_RATE,
        "bonus_available": remaining_allowance * LISA_BONUS_RATE,
        "limit": LISA_ANNUAL_LIMIT,
    }


def isa_allowance_status(contributions, isa_account_ids, today=None):
    label, start, end = current_tax_year(today)
    used = sum(
        contributions_in_range(contributions, acc_id, start, end)
        for acc_id in isa_account_ids
    )
    return {
        "tax_year": label,
        "used": used,
        "allowance": ISA_ANNUAL_ALLOWANCE,
        "remaining": max(ISA_ANNUAL_ALLOWANCE - used, 0),
    }


def growth_vs_contribution(history, contributions, account_id, start_month, end_month):
    def balance_at(month):
        for h in history:
            if h["month"] == month:
                return h.get("balances", {}).get(account_id)
        return None

    start_balance = balance_at(start_month)
    end_balance = balance_at(end_month)
    if start_balance is None or end_balance is None:
        return None

    start_date = date.fromisoformat(start_month + "-01")
    end_date = date.fromisoformat(end_month + "-01")
    if start_month != end_month:
        # Contributions are included from the start month through the end month.
        if end_date.month == 12:
            range_end = date(end_date.year + 1, 1, 1)
        else:
            range_end = date(end_date.year, end_date.month + 1, 1)
        range_end = range_end.fromordinal(range_end.toordinal() - 1)
    else:
        range_end = end_date

    contributed = contributions_in_range(
        contributions, account_id, start_date, range_end
    )
    change = float(end_balance) - float(start_balance)
    return {
        "start_balance": float(start_balance),
        "end_balance": float(end_balance),
        "change": change,
        "contributed": contributed,
        "growth": change - contributed,
    }


def average_monthly_contribution(contributions, account_ids=None, months=3, today=None):
    today = today or date.today()
    total = 0.0
    for c in contributions:
        c_date = date.fromisoformat(c["date"])
        age_months = (today.year - c_date.year) * 12 + today.month - c_date.month
        if 0 <= age_months < months and (account_ids is None or c["account_id"] in account_ids):
            total += float(c.get("amount", 0))
    return total / months if months else 0


def project(current_total, monthly_contribution, annual_growth_pct, years):
    values = [float(current_total)]
    value = float(current_total)
    for _ in range(years):
        monthly_rate = (1 + annual_growth_pct / 100) ** (1 / 12) - 1
        for _ in range(12):
            value = value * (1 + monthly_rate) + monthly_contribution
        values.append(value)
    return values


def projection_breakdown(current_total, monthly_contribution, annual_growth_pct, years):
    final_value = project(current_total, monthly_contribution, annual_growth_pct, years)[-1]
    contributions = monthly_contribution * 12 * years
    growth = final_value - current_total - contributions
    return {
        "final_value": final_value,
        "contributions": contributions,
        "growth": growth,
    }


def months_to_target(current_total, monthly_contribution, annual_growth_pct, target, max_months=600):
    if current_total >= target:
        return 0
    monthly_growth = (1 + annual_growth_pct / 100) ** (1 / 12) - 1
    value = float(current_total)
    for month in range(1, max_months + 1):
        value = value * (1 + monthly_growth) + monthly_contribution
        if value >= target:
            return month
    return None
