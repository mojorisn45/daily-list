from __future__ import annotations

from datetime import date, timedelta
from itertools import groupby

import streamlit as st

import db


def _label_for(d: date, today: date) -> str:
    if d == today:
        return f"Today — {d.strftime('%B %-d') if _has_dash_d() else d.strftime('%B %d').lstrip('0')}"
    if d == today - timedelta(days=1):
        return f"Yesterday — {_day_month(d)}"
    return f"{d.strftime('%A')} — {_day_month(d)}"


def _has_dash_d() -> bool:
    try:
        date(2026, 4, 1).strftime("%-d")
        return True
    except ValueError:
        return False


def _day_month(d: date) -> str:
    return f"{d.strftime('%B')} {d.day}"


def render() -> None:
    tasks = db.get_archive(days=30)
    if not tasks:
        st.info("Archive is empty. Complete a task today, then check back tomorrow.")
        return

    today = db.today_local()
    for archived_date_str, group in groupby(tasks, key=lambda t: t["archived_date"]):
        try:
            d = date.fromisoformat(archived_date_str)
        except (TypeError, ValueError):
            continue
        st.caption(_label_for(d, today).upper())
        for t in group:
            recurring_mark = " 🔁" if t.get("recurring_id") else ""
            st.markdown(f"✅ {t['text']}{recurring_mark}")
        st.write("")
