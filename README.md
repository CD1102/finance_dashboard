# Finance Dashboard

A personal finance analytics dashboard built with Python + Streamlit. The application is designed to be genuinely useful day-to-day while also serving as the workload for a wider cloud engineering learning project.

## Current application

- Dashboard with current net worth, allocation, account cards and interactive charts
- One-click balance updates from the dashboard
- Monthly snapshots and historical net-worth tracking
- Account-level history filters
- Contribution logging and a contribution history table
- Goal tracking
- LISA bonus and ISA allowance tracking
- Scenario-based projections with nominal vs inflation-adjusted values
- Goal time-to-target calculator
- JSON data layer deliberately separated from calculations so it can later be replaced by a database

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Data privacy

Real personal data files are gitignored. The `*.example.json` files are safe templates. Do not commit real balances to a public repository.

## Project direction

The application is the workload; the main engineering learning goal is the path from local application to reliable cloud service:

```text
Streamlit app
   -> Git / GitHub
   -> Docker
   -> GitHub Actions (CI/CD)
   -> Azure Container Registry
   -> Azure hosting
   -> Infrastructure as Code
   -> secrets / identity
   -> persistent storage
   -> monitoring / logging
   -> cost management
```

The current release focuses on a usable dashboard and historical workflow. The next phase is deployment and infrastructure rather than adding endless front-end features.
