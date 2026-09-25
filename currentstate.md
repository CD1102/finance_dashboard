PROJECT CONTEXT — FINANCE DASHBOARD / CLOUD ENGINEERING

I am building a personal finance Streamlit application as a real application I will use, while using the project to learn cloud/platform engineering.

Current repo:
https://github.com/CD1102/finance_dashboard

Local repo:
C:\Users\joshd\finance_dashboard

Environment:
- Windows ARM64
- VS Code
- PowerShell
- Existing Python .venv
- Git/GitHub working
- Docker Desktop installed
- WSL2 installed and working
- Docker daemon confirmed working
- `docker run hello-world` successfully ran an ARM64 container

IMPORTANT:
I am NOT an apprentice anymore. My current role is Service Analytics & Automation Analyst.

APPLICATION:
The app is a personal financial command centre, not a transaction tracker.

It should eventually provide:
- Current net worth
- Net worth history
- Investments/cash/pension split
- Account balances and account history
- Monthly income/spending/savings
- Savings rate
- Contributions vs investment/interest movement where data supports it
- Goals
- Goal progress
- Financial projections/scenarios
- Historical yearly/monthly analysis
- Import of historical Excel/CSV data
- Export/backup
- High-quality modern SaaS-style UI
- Interactive Plotly charts
- Clean data/business-logic/UI separation

I don't want to track every transaction. I currently use a monthly finance spreadsheet and want the app to become a much nicer frontend/analytical layer for it.

DATA:
Currently JSON is acceptable for the prototype, but the architecture should allow:
JSON → SQLite/database → Azure persistent storage/database.

Real financial data must NEVER be committed to the public GitHub repository.

The app should eventually be:
GitHub
→ Docker
→ Azure Container Apps
→ GitHub Actions CI/CD
→ IaC
→ secure secrets/identity
→ persistent database/storage
→ monitoring/logging
→ cost management

DEPLOYMENT STATUS:
DONE:
- GitHub repo
- Git
- Docker Desktop
- WSL2
- Docker daemon
- Successfully ran `docker run hello-world`

NEXT DEPLOYMENT STEP:
Containerise the actual finance application.

Expected immediate sequence:
1. Create Dockerfile
2. Create appropriate .dockerignore
3. Build Docker image
4. Run finance app in Docker locally
5. Verify it works at localhost:8501
6. Then move toward Azure Container Apps

IMPORTANT LEARNING PREFERENCE:
For Python/application code, I am happy for a strong coding model to generate/copy-paste code.

My main learning goals are:
- Docker
- Git
- CI/CD
- Azure
- Infrastructure
- IaC
- Secrets/identity
- Databases
- Monitoring
- Cost management
- Deployment

Therefore explain the infrastructure concepts and WHY we are doing things, but don't unnecessarily slow down basic Python implementation.

I prefer practical, exact, non-overwhelming instructions.

IMPORTANT:
Before asking me to install any new software/tool, tell me beforehand that it needs to be installed.

Also, don't troubleshoot by throwing 10 possible fixes at me. Diagnose one thing at a time.

CURRENT POSITION:
Docker has just been successfully tested with hello-world. We stopped here intentionally.

Next task: containerise the actual finance dashboard.
