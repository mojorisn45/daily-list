from __future__ import annotations

import streamlit as st

import db


def _submit_new_recurring() -> None:
    text = st.session_state.get("new_recurring_input", "").strip()
    if not text:
        return
    db.add_recurring(text)
    st.session_state["new_recurring_input"] = ""


def render() -> None:
    templates = db.get_recurring_templates()

    st.caption("DAILY RECURRING · auto-adds to Today each morning")

    if not templates:
        st.info("No daily recurring tasks yet. Add one below.")
    else:
        for t in templates:
            c1, c2 = st.columns([6, 2])
            c1.markdown(t["text"])
            if c2.button("Remove", key=f"rm_{t['id']}", use_container_width=True):
                db.remove_recurring(t["id"])
                st.rerun()

    st.divider()

    st.text_input(
        "New recurring task",
        key="new_recurring_input",
        placeholder="Add daily recurring task...",
        label_visibility="collapsed",
        on_change=_submit_new_recurring,
    )
    if st.button("Add recurring", type="primary"):
        _submit_new_recurring()
        st.rerun()
