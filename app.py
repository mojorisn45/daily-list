from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Daily List", page_icon="📋", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700&display=swap');

    :root {
        --bg: #FBFAF6;
        --surface: #F2F0E9;
        --text: #17170F;
        --text-muted: #76736B;
        --border: #E8E5DC;
        --border-strong: #D6D1C3;
        --accent: #15803D;
        --accent-hover: #0F6B33;
        --accent-soft: #DCFCE7;
        --recurring: #B45309;
        --recurring-soft: #FEF3C7;
        --park: #B45309;
    }

    /* --- Typography --- */
    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {
        font-family: 'Instrument Sans', -apple-system, system-ui, sans-serif !important;
    }

    .stApp { background-color: var(--bg); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppDeployButton"] { display: none !important; }
    footer { display: none !important; }

    .block-container {
        max-width: 480px !important;
        padding: 1.5rem 1.25rem 5rem !important;
    }

    /* --- Headings --- */
    [data-testid="stMarkdownContainer"] h1 {
        font-weight: 600;
        font-size: 1.875rem;
        letter-spacing: -0.02em;
        color: var(--text);
        margin: 0 0 0.125rem;
    }

    /* --- Body paragraphs (task text, etc) --- */
    [data-testid="stMarkdownContainer"] p {
        font-size: 1.125rem;
        font-weight: 600;
        line-height: 1.4;
        color: var(--text);
        margin: 0;
        letter-spacing: -0.005em;
    }

    /* Button text should inherit button color, not body text color */
    .stButton button [data-testid="stMarkdownContainer"] p {
        color: inherit !important;
        font-size: 0.9375rem !important;
        font-weight: 500 !important;
    }
    .stButton > button[data-testid="stBaseButton-primary"] [data-testid="stMarkdownContainer"] p {
        color: white !important;
        font-weight: 600 !important;
    }

    /* --- Captions (date, section labels) --- */
    [data-testid="stCaptionContainer"] p,
    .stCaption p {
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    /* Colored bullet before section labels that start with TODAY / DAILY RECURRING */
    [data-testid="stCaptionContainer"] p::before {
        content: "";
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--accent);
        margin-right: 0.6em;
        vertical-align: middle;
        transform: translateY(-1px);
    }
    /* Date rendered as plain HTML div to bypass caption styling */
    .app-date {
        color: var(--text-muted);
        font-size: 0.9375rem;
        font-weight: 400;
        margin-bottom: 0.75rem;
        letter-spacing: 0;
    }

    /* --- Checkboxes: bigger visual square --- */
    div[data-testid="stCheckbox"] { padding: 4px 0; }
    div[data-testid="stCheckbox"] label {
        min-height: 38px;
        align-items: center;
        gap: 0.5rem;
    }
    div[data-testid="stCheckbox"] label > div:first-child,
    div[data-testid="stCheckbox"] label > span:first-child {
        min-width: 26px !important;
        min-height: 26px !important;
        width: 26px !important;
        height: 26px !important;
        border-radius: 7px !important;
        border: 2px solid var(--border-strong) !important;
        background-color: var(--bg) !important;
        transition: all 0.15s ease;
    }
    /* Checked state: fill with accent, white checkmark */
    div[data-testid="stCheckbox"] label:has(input:checked) > div:first-child,
    div[data-testid="stCheckbox"] label:has(input:checked) > span:first-child {
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
    }
    div[data-testid="stCheckbox"] label:has(input:checked) svg {
        color: white !important;
        fill: white !important;
    }

    /* --- Buttons --- */
    .stButton > button,
    [data-testid="stBaseButton-secondary"] {
        font-family: 'Instrument Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9375rem !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-strong) !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
        padding: 0.5rem 0.875rem !important;
        min-height: 42px !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        background-color: var(--surface) !important;
        border-color: var(--text-muted) !important;
        color: var(--text) !important;
    }
    /* Primary button needs higher specificity to beat .stButton > button */
    .stButton > button[data-testid="stBaseButton-primary"] {
        background-color: var(--accent) !important;
        border: 1px solid var(--accent) !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        min-height: 42px !important;
        padding: 0.5rem 0.875rem !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: var(--accent-hover) !important;
        border-color: var(--accent-hover) !important;
        color: white !important;
    }

    /* --- Text input --- */
    [data-testid="stTextInput"] input {
        font-family: 'Instrument Sans', sans-serif !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-strong) !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
        padding: 0.75rem 0.875rem !important;
        min-height: 46px !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
        outline: none !important;
    }

    /* --- Progress bar (base-web nested structure) --- */
    [data-baseweb="progress-bar"] > div {
        background-color: var(--border) !important;
        border-radius: 999px !important;
    }
    [data-baseweb="progress-bar"] > div > div > div {
        background-color: var(--accent) !important;
        border-radius: 999px !important;
    }

    /* --- Tabs --- */
    .stTabs [role="tablist"] {
        gap: 1.5rem;
        border-bottom: 1px solid var(--border);
    }
    .stTabs button[role="tab"] {
        font-family: 'Instrument Sans', sans-serif !important;
        font-size: 0.9375rem !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        padding: 0.625rem 0 !important;
        background: transparent !important;
    }
    .stTabs button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
    }
    /* The red bar under the active tab is a separate element */
    [data-baseweb="tab-highlight"] {
        background-color: var(--accent) !important;
    }
    [data-baseweb="tab-border"] {
        background-color: var(--border) !important;
    }
    [role="tabpanel"] { padding-top: 1.25rem; }

    /* --- Expander --- */
    [data-testid="stExpander"] details {
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        background-color: var(--surface) !important;
    }
    [data-testid="stExpander"] summary {
        font-family: 'Instrument Sans', sans-serif !important;
        font-size: 0.9375rem !important;
        font-weight: 500 !important;
        color: var(--text) !important;
        padding: 0.875rem 1rem !important;
    }

    /* --- Radio (Today / Parking Lot toggle) styled as pill switch --- */
    [data-testid="stRadio"] {
        width: 100% !important;
    }
    [data-testid="stRadio"] > div {
        flex-direction: row !important;
        gap: 0.5rem !important;
        width: 100% !important;
    }
    [data-testid="stRadio"] label {
        flex: 1 1 0 !important;
        padding: 0.5rem 0.75rem;
        border: 1px solid var(--border-strong);
        border-radius: 10px;
        background: var(--bg);
        cursor: pointer;
        transition: all 0.15s ease;
        justify-content: center;
        font-weight: 500;
        min-height: 44px;
        white-space: nowrap;
    }
    [data-testid="stRadio"] label:hover {
        background: var(--surface);
    }
    [data-testid="stRadio"] label:has(input:checked) {
        background: var(--text);
        color: white;
        border-color: var(--text);
    }
    [data-testid="stRadio"] label:has(input:checked) p {
        color: white !important;
    }
    [data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* --- Divider --- */
    hr, [data-testid="stDivider"] {
        border-color: var(--border) !important;
        margin: 1.25rem 0 !important;
    }

    /* --- Alert / info (empty states) --- */
    [data-testid="stAlert"],
    [data-testid="stAlertContainer"] {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-muted) !important;
        padding: 1rem 1.25rem !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlertContainer"] p {
        color: var(--text-muted) !important;
        font-weight: 400 !important;
    }

    /* --- Horizontal block (columns) --- */
    [data-testid="stHorizontalBlock"] {
        align-items: center;
        gap: 0.75rem;
    }

    div[data-testid="stVerticalBlock"] { gap: 0.5rem; }

    /* Force widget containers full-width so radios / pills stretch across the row */
    [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] {
        width: 100% !important;
        min-width: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

import importlib

import db
from rollover import run_rollover_if_needed
from views import archive as archive_view
from views import recurring as recurring_view
from views import today as today_view

# Streamlit Cloud caches submodule imports across reruns — a git push of
# only views/*.py does not reliably flush them. Force reload so layout
# edits land without a manual app reboot.
importlib.reload(today_view)
importlib.reload(archive_view)
importlib.reload(recurring_view)
importlib.reload(db)
importlib.reload(__import__("rollover"))

run_rollover_if_needed()

today_date = db.today_local()
st.markdown("# Daily List")
st.markdown(
    f"<div class='app-date'>{today_date.strftime('%A, %B %d, %Y')}</div>",
    unsafe_allow_html=True,
)

tab_today, tab_archive, tab_recurring = st.tabs(["Today", "Archive", "Recurring"])
with tab_today:
    today_view.render()
with tab_archive:
    archive_view.render()
with tab_recurring:
    recurring_view.render()
