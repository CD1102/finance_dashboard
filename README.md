You are working on my existing personal finance application repository.

IMPORTANT:
Do not immediately rewrite the application.
First inspect the entire repository and understand the existing architecture, files, functionality, data model, dependencies and current UI.

The goal is to turn this into a genuinely excellent personal financial command centre that I will actually use, rather than a generic Streamlit demo.

==================================================
PRODUCT VISION
==================================================

Build a polished personal finance application using Streamlit.

The application should answer one main question:

"How am I doing financially, and where am I heading?"

This is NOT intended to be a transaction-by-transaction budgeting app.

My current system is essentially a monthly financial spreadsheet. I track monthly totals and account balances rather than every individual transaction.

The application should therefore become a much better frontend and analytical layer for that system.

Think:

PERSONAL FINANCIAL COMMAND CENTRE

rather than:

BASIC BUDGET TRACKER

The application should eventually feel like a polished SaaS financial product.

==================================================
FIRST: INSPECT THE EXISTING REPOSITORY
==================================================

Before changing anything:

1. Inspect all relevant files.
2. Understand the current Streamlit architecture.
3. Identify the current pages.
4. Understand the existing data files.
5. Understand the existing calculations.
6. Understand how historical data currently works.
7. Understand how goals and projections currently work.
8. Inspect requirements/dependencies.
9. Identify anything that should be preserved.
10. Identify technical debt or architectural weaknesses.

Do NOT throw away working functionality simply to rewrite it.

After inspection, provide a concise proposed architecture and implementation plan.

Then implement the improvements in logical phases.

Do not generate a giant untested rewrite.

Test the application after meaningful changes.

==================================================
CORE USER EXPERIENCE
==================================================

When I open the application, I should immediately understand:

- My current net worth
- Whether my net worth is increasing/decreasing
- Where my money currently sits
- How much progress I've made toward important goals
- Whether my current trajectory is broadly on track
- What happened financially during the current month
- How my current position compares with previous months/years

The dashboard should prioritise useful information over simply displaying lots of numbers.

==================================================
HOME / FINANCIAL OVERVIEW
==================================================

Create a genuinely polished overview page.

The most important information should be visible without excessive navigation.

Potential primary metrics:

- Total net worth
- Monthly net worth change (£)
- Monthly net worth change (%)
- Investments
- Cash/savings
- Pension
- Savings rate
- Monthly income
- Monthly spending
- Monthly contributions
- Goal progress
- Emergency fund position
- Current trajectory

Use sensible prioritisation and visual hierarchy rather than displaying every metric equally.

Include:

1. Net worth hero section

2. Financial allocation

Show the split between:
- Investments
- Cash/savings
- Pension
- Other assets if applicable

3. Net worth history

Interactive Plotly chart.

Allow useful periods such as:
- 1 month
- 3 months
- 6 months
- 1 year
- 3 years
- all available history

Hovering should provide useful information.

4. Monthly financial summary

Show:
- Income
- Spending
- Savings/investment contributions
- Remaining/other

5. Goal progress

Show the most important active goals without overwhelming the dashboard.

6. Recent financial movement

Explain what changed rather than just displaying numbers.

For example:

"Net worth increased £X this month."

"£X was added through contributions."

"Investments changed by approximately £X."

Only make statements that can actually be supported by the stored data.

==================================================
ACCOUNTS
==================================================

Create an account view that is substantially more useful than a simple list.

Each account should support metadata such as:

- Name
- Account type
- Category
- Purpose
- Current balance
- Contribution amount
- Interest/return information where applicable
- Historical balances

Categories may include:

- Investment
- Cash/Savings
- Pension
- Other

Clicking/selecting an account should allow me to see its history.

For example:

S&S ISA

Current balance: £X

Monthly contribution: £X

Historical balance chart

Change over selected period

Contribution information where available

Do not hard-code specific account names into the architecture.

Accounts must be configurable.

==================================================
MONTHLY FINANCE
==================================================

This replaces the useful parts of my existing spreadsheet.

The application should allow me to record one monthly financial snapshot rather than requiring transaction-level tracking.

A monthly record can contain:

INCOME
- Total income

SPENDING
- Total spending
- Optional high-level categories

SAVING / INVESTING
- Investments
- Cash savings
- Pension contributions
- Other contributions

ACCOUNT BALANCES
- Balance for each configured account

The application should calculate useful derived metrics automatically.

Examples:

Savings rate

Contribution rate

Monthly surplus

Net worth change

Year-to-date totals

Annual totals

Monthly averages

Do not turn this into a transaction management system unless there is a strong architectural reason to do so.

==================================================
HISTORICAL DATA
==================================================

Historical data is important.

I want to be able to see:

- Previous months
- Previous years
- Annual comparisons
- Long-term net worth progression
- Income progression
- Spending progression
- Savings progression
- Contribution progression

The UI should make historical analysis easy.

Allow useful filtering by:

- Date
- Year
- Account
- Category

Where appropriate.

==================================================
HISTORICAL IMPORT
==================================================

I currently have historical financial information stored in an Excel spreadsheet.

The application should eventually support importing historical data from:

- Excel
- CSV

The import workflow should be safe.

Ideally:

Upload file
→ inspect columns
→ map fields
→ preview imported records
→ validate
→ confirm import

Do NOT automatically overwrite existing financial data.

Provide appropriate validation and confirmation.

Historical imports should be designed so that they can be repeated safely.

==================================================
INVESTMENT PERFORMANCE
==================================================

Where sufficient data exists, distinguish between:

- Money I contributed
- Investment growth/loss
- Interest earned
- Net worth change

For example:

Net worth increased £1,200

Contributions: +£1,000

Investment/interest movement: +£200

Do not pretend to know investment performance if the available data cannot support the calculation.

Clearly distinguish:

KNOWN DATA

from

CALCULATED DATA

from

ASSUMPTIONS / PROJECTIONS

==================================================
GOALS
==================================================

Create a proper goals system.

Goals could include:

- Net worth target
- House deposit
- Cash target
- Investment target
- Other financial target

Each goal should support:

- Name
- Target amount
- Current amount
- Target date
- Description
- Optional monthly contribution assumption

Display:

- Current progress
- Percentage complete
- Amount remaining
- Required contribution where calculable
- Projected completion date where appropriate

Do not imply certainty about future outcomes.

==================================================
PROJECTIONS
==================================================

Create an interactive projection system.

Allow assumptions such as:

- Current net worth
- Monthly contributions
- Expected investment return
- Cash interest rate
- Inflation
- Contribution growth
- Time horizon

Show projected financial trajectory.

Allow scenario exploration.

For example:

Current contribution rate
vs
Higher contribution rate
vs
Custom scenario

Separate:

- Starting wealth
- Contributions
- Investment growth
- Interest
- Total projected value

Clearly label all projections as projections.

Do not present assumptions as facts.

Make the model transparent enough that I can understand how the projection is produced.

==================================================
BUDGETING
==================================================

I do want high-level budgeting, but NOT transaction tracking.

Allow monthly values such as:

Income
Spending
Savings
Investments
Other financial commitments

Optional spending categories can include things like:

- Bills
- Transport
- Food
- Subscriptions
- Giving
- Shopping
- Other

The purpose is to understand monthly financial behaviour, not to reconcile every transaction.

The application should eventually let me see:

Income → spending → saving/investing

and derive useful statistics such as:

- Savings rate
- Average monthly spending
- Annual spending
- Monthly surplus
- Spending trends
- Contribution trends

==================================================
DATA ARCHITECTURE
==================================================

Do NOT tightly couple the UI to JSON files.

Use a clear separation such as:

UI
↓
Business / calculation logic
↓
Data access layer
↓
Storage

JSON is acceptable for the early prototype.

However, design the data layer so that it can eventually transition to:

JSON
→ SQLite
→ persistent cloud database/storage

without requiring the entire application to be rewritten.

Do not scatter file-reading/writing logic throughout Streamlit pages.

Keep calculations separate from UI code.

Keep data models/configuration separate from presentation where practical.

==================================================
DATA SAFETY
==================================================

This application contains sensitive personal financial information.

NEVER hard-code my real financial information into source code.

NEVER put real financial data into files intended for public GitHub.

Ensure .gitignore protects local financial data.

Use example/template data where appropriate.

Make it easy to export/backup my data.

The application should eventually support a clean transition to secure persistent cloud storage.

==================================================
IMPORT / EXPORT / BACKUP
==================================================

Consider a dedicated data/settings area.

Capabilities should eventually include:

- Add/edit accounts
- Add/edit goals
- Add monthly snapshot
- Import historical data
- Export data
- Backup data
- View data status

Do not make these features clutter the main dashboard.

==================================================
DESIGN / UI
==================================================

This is extremely important.

Do NOT make this look like a basic Streamlit tutorial.

Treat it as a real financial SaaS application.

Use Streamlit properly and push the UI as far as is sensible without introducing unnecessary complexity.

Desired qualities:

- Strong visual hierarchy
- Modern dashboard layout
- Clean typography
- Consistent spacing
- Professional cards
- Excellent use of whitespace
- Interactive Plotly charts
- Useful hover states
- Responsive layout where practical
- Clear navigation
- Clean forms
- Good empty states
- Useful validation messages
- Clear success/error feedback
- Sensible filters
- Polished tables
- Consistent component design
- Dark/light support where practical

Avoid:

- Giant walls of text
- Excessive cards
- Redundant metrics
- Raw JSON visible to users
- Developer terminology
- Fake analytics
- Decorative charts with no analytical purpose
- Excessive emojis
- Overly complicated navigation
- Features that exist only because they look impressive

The interface should feel calm, useful and premium.

==================================================
STREAMLIT ENGINEERING
==================================================

Use Streamlit idiomatically.

Prefer reusable components/functions over duplicating UI code.

Use session state appropriately.

Use caching appropriately.

Avoid unnecessary reruns.

Use Plotly for interactive analytical charts.

Keep page-specific code reasonably thin.

Do not introduce a frontend framework such as React unless there is a compelling reason and I explicitly approve it.

The goal is to make the best practical application possible within Streamlit.

==================================================
CALCULATIONS
==================================================

Centralise financial calculations.

Examples:

- Total net worth
- Allocation percentages
- Monthly change
- Monthly percentage change
- Savings rate
- Contribution totals
- Annual totals
- Goal progress
- Required contribution
- Projection values

Calculations should be testable independently from Streamlit.

Avoid duplicating financial logic across pages.

==================================================
QUALITY / TESTING
==================================================

Do not just make the application "look right."

Validate that calculations are correct.

Add tests for important financial calculations where practical.

Test edge cases such as:

- Missing data
- Empty history
- Zero income
- Zero balances
- Negative monthly movement
- New account
- Missing historical months
- Goals without target dates
- Projection with zero contributions

The application should fail gracefully rather than crash.

==================================================
IMPORTANT PRODUCT PRINCIPLES
==================================================

1. Useful beats impressive.

2. Accuracy beats visual decoration.

3. Historical data is extremely important.

4. Do not require transaction-level tracking.

5. Do not assume future returns.

6. Make calculations transparent.

7. Protect personal financial data.

8. Keep the architecture ready for database/cloud migration.

9. Do not unnecessarily rewrite working code.

10. Build incrementally and test after each major change.

==================================================
CLOUD / FUTURE ARCHITECTURE
==================================================

The application will eventually be:

GitHub
→ Docker
→ Azure Container Apps
→ CI/CD
→ Infrastructure as Code
→ secure persistent storage/database
→ monitoring

Do not implement all of that now unless it is already present.

However, make architectural decisions that will not make those future steps unnecessarily difficult.

The application must remain container-friendly.

Do not introduce dependencies that cannot reasonably run in a Docker/Linux environment.

==================================================
WORKING STYLE
==================================================

Before implementation:

1. Inspect the repository.
2. Summarise the current architecture.
3. Identify what is already good.
4. Identify the biggest weaknesses.
5. Propose the implementation phases.

Then work through the phases.

Do not ask me unnecessary questions if the repository already contains enough information to make a reasonable decision.

When a decision genuinely affects the product architecture, explain the decision briefly and choose a sensible default.

Do not create enormous amounts of code in one step without testing.

After each major phase:

- run the appropriate tests
- check for syntax/import errors
- check the Streamlit application
- report what changed
- report anything that still needs attention

Most importantly:

Build this as an application I would genuinely want to open every month to understand my financial position.

Do not optimise for "portfolio demo."

Optimise for:

REAL PERSONAL USE
+
EXCELLENT UX
+
GOOD FINANCIAL DATA MODEL
+
CLEAN SOFTWARE ARCHITECTURE
+
FUTURE CLOUD DEPLOYMENT
