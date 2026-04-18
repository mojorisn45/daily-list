from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Daily List", page_icon="📋", layout="centered")

st.markdown(
    """
    <style>
    .block-container {max-width: 480px; padding-top: 1.5rem; padding-bottom: 5rem;}
    [data-testid="stHorizontalBlock"] {align-items: center;}
    div[data-testid="stVerticalBlock"] {gap: 0.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

from auth import require_password

require_password()

import db
from rollover import run_rollover_if_needed
from views import archive as archive_view
from views import recurring as recurring_view
from views import today as today_view

run_rollover_if_needed()

today_date = db.today_local()
st.markdown("# 📋 Daily List")
st.caption(today_date.strftime("%A, %B %d, %Y"))

tab_today, tab_archive, tab_recurring = st.tabs(["Today", "Archive", "Recurring"])
with tab_today:
    today_view.render()
with tab_archive:
    archive_view.render()
with tab_recurring:
    recurring_view.render()
