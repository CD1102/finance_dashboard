"""Shared visual system for the Finance Dashboard."""

import streamlit as st

TYPE_COLORS = {
    "investment": "#22C55E",
    "cash": "#38BDF8",
    "pension": "#A78BFA",
}

TYPE_ICONS = {
    "investment": "📈",
    "cash": "💷",
    "pension": "🏦",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

h1, h2, h3 { font-weight: 800 !important; letter-spacing: -0.025em; }
h1 { font-size: 2.2rem !important; }
h2 { font-size: 1.45rem !important; }
h3 { font-size: 1.05rem !important; }

[data-testid="stMetricValue"] {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

[data-testid="stMetricLabel"] {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #8B949E;
    font-weight: 700;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border-color: #29313C !important;
    background: #121820;
}

.stButton > button, .stFormSubmitButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 2.55rem;
}

div[data-testid="stPopover"] button {
    border-radius: 10px;
    font-weight: 700;
}

.section-title {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #8B949E;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.hero {
    background: radial-gradient(circle at 90% 15%, rgba(34,197,94,0.30), transparent 34%),
                linear-gradient(135deg, #0F3D2B 0%, #0B221A 100%);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 22px;
    padding: 1.65rem 1.85rem;
    margin: 0.5rem 0 1.25rem 0;
}

.hero-label { color: #A7F3D0; font-size: 0.76rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; }
.hero-value { color: #F0FFF8; font-size: 3rem; line-height: 1; font-weight: 800; letter-spacing: -0.045em; margin-top: 0.25rem; }
.hero-meta { color: #B9DCCB; font-size: 0.88rem; margin-top: 0.65rem; font-weight: 600; }

.mini-card {
    border: 1px solid #29313C;
    background: #121820;
    border-radius: 16px;
    padding: 1rem 1.05rem;
}
.mini-label { color: #8B949E; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 800; }
.mini-value { color: #F3F4F6; font-size: 1.35rem; font-weight: 800; margin-top: 0.15rem; }
.mini-sub { color: #8B949E; font-size: 0.76rem; margin-top: 0.25rem; }

.account-card {
    border: 1px solid #29313C;
    background: linear-gradient(180deg, #151C25 0%, #11171E 100%);
    border-radius: 16px;
    padding: 1rem;
    min-height: 122px;
}
.account-card .icon { font-size: 1.3rem; }
.account-card .name { font-size: 0.82rem; color: #A8B1BC; font-weight: 700; margin-top: 0.55rem; }
.account-card .value { font-size: 1.28rem; color: #F5F7FA; font-weight: 800; margin-top: 0.12rem; }
.account-card .share { font-size: 0.74rem; color: #7F8A97; margin-top: 0.2rem; }

.kpi-good { color: #86EFAC; }
.kpi-muted { color: #94A3B8; }
.kpi-bad { color: #FCA5A5; }

[data-testid="stProgress"] > div > div {
    height: 10px;
    border-radius: 999px;
}
[data-testid="stProgress"] > div { border-radius: 999px; }

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

.small-note { color: #8B949E; font-size: 0.78rem; line-height: 1.45; }

.divider { height: 1px; background: #242C36; margin: 1.4rem 0; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(value_str, delta_str=None, positive=True, subtitle="Current financial position"):
    if delta_str:
        delta_class = "kpi-good" if positive else "kpi-bad"
        arrow = "↑" if positive else "↓"
        delta_html = f'<span class="{delta_class}">{arrow} {delta_str}</span>'
    else:
        delta_html = '<span class="kpi-muted">No previous snapshot yet</span>'

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-label">Total Net Worth</div>
            <div class="hero-value">{value_str}</div>
            <div class="hero-meta">{subtitle} · {delta_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def account_card(icon, name, balance, percentage):
    st.markdown(
        f"""
        <div class="account-card">
            <div class="icon">{icon}</div>
            <div class="name">{name}</div>
            <div class="value">£{balance:,.0f}</div>
            <div class="share">{percentage:.0f}% of net worth</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_layout(fig, height=340, showlegend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF3", family="Manrope, sans-serif"),
        margin=dict(l=8, r=8, t=28, b=10),
        height=height,
        hoverlabel=dict(bgcolor="#111827", bordercolor="#374151", font_color="#F8FAFC"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ) if showlegend else None,
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color="#8B949E")
    fig.update_yaxes(gridcolor="#202833", zeroline=False, color="#8B949E")
    return fig
