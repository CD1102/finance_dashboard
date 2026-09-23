"""Data access layer.

The pages only call these functions. When JSON is eventually replaced with a
real database, this is the main layer that changes.
"""

import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"
HISTORY_FILE = DATA_DIR / "history.json"
CONTRIBUTIONS_FILE = DATA_DIR / "contributions.json"
GOALS_FILE = DATA_DIR / "goals.json"


def _load(path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _save(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_accounts_full():
    return _load(ACCOUNTS_FILE, {"accounts": [], "last_updated": None})


def load_accounts():
    return load_accounts_full().get("accounts", [])


def save_accounts(accounts):
    _save(ACCOUNTS_FILE, {
        "accounts": accounts,
        "last_updated": date.today().isoformat(),
    })


def update_balance(account_id, new_balance):
    accounts = load_accounts()
    for acc in accounts:
        if acc["id"] == account_id:
            acc["balance"] = float(new_balance)
            break
    save_accounts(accounts)
    return accounts


def load_history():
    return _load(HISTORY_FILE, [])


def save_history(history):
    _save(HISTORY_FILE, history)


def add_snapshot(month, balances_by_id):
    history = [h for h in load_history() if h["month"] != month]
    history.append({
        "month": month,
        "balances": {k: float(v) for k, v in balances_by_id.items()},
    })
    history.sort(key=lambda h: h["month"])
    save_history(history)
    return history


def load_contributions():
    return _load(CONTRIBUTIONS_FILE, [])


def save_contributions(contributions):
    _save(CONTRIBUTIONS_FILE, contributions)


def log_contribution(entry_date, account_id, amount, note=""):
    contributions = load_contributions()
    contributions.append({
        "date": entry_date,
        "account_id": account_id,
        "amount": float(amount),
        "note": note,
    })
    contributions.sort(key=lambda c: c["date"])
    save_contributions(contributions)
    return contributions


def load_goals():
    return _load(GOALS_FILE, [])


def save_goals(goals):
    _save(GOALS_FILE, goals)


def update_goal_field(goal_id, field, value):
    goals = load_goals()
    for goal in goals:
        if goal["id"] == goal_id:
            goal[field] = value
            break
    save_goals(goals)
    return goals
