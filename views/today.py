from __future__ import annotations

import streamlit as st

import db


_BADGE_HTML = (
    "<span style='display:inline-block;background:var(--recurring-soft);"
    "color:var(--recurring);font-size:0.6875rem;font-weight:700;"
    "text-transform:uppercase;letter-spacing:0.08em;"
    "padding:2px 8px;border-radius:999px;margin-left:8px;"
    "vertical-align:middle;'>daily</span>"
)


def _is_recurring(t: dict) -> bool:
    return t.get("recurring_id") is not None


def _submit_quick_add() -> None:
    text = st.session_state.get("quick_add_input", "").strip()
    if not text:
        return
    target = st.session_state.get("quick_add_target", "Today")
    list_name = "today" if target == "Today" else "parking"
    db.add_task(text, list_name)
    st.session_state["quick_add_input"] = ""


def _render_progress(open_count: int, done_count: int) -> None:
    total = open_count + done_count
    pct = int(round(done_count / total * 100)) if total else 0
    st.markdown(f"**{done_count} / {total} completed**")
    st.progress(pct / 100)


def _render_quick_add() -> None:
    st.text_input(
        "Add a task",
        key="quick_add_input",
        placeholder="Add a task...",
        label_visibility="collapsed",
        on_change=_submit_quick_add,
    )
    st.radio(
        "Target",
        ["Today", "Parking Lot"],
        key="quick_add_target",
        horizontal=True,
        label_visibility="collapsed",
    )
    if st.button("Add", use_container_width=True, type="primary"):
        _submit_quick_add()
        st.rerun()


def _render_open_tasks(tasks: list[dict]) -> None:
    if not tasks:
        st.info("All done for today.")
        return
    for t in tasks:
        c1, c2, c3 = st.columns([1, 6, 2])
        done_now = c1.checkbox(
            "done",
            value=False,
            key=f"done_{t['id']}",
            label_visibility="collapsed",
        )
        if done_now:
            db.set_done(t["id"], True)
            st.rerun()
        badge = _BADGE_HTML if _is_recurring(t) else ""
        c2.markdown(f"{t['text']}{badge}", unsafe_allow_html=True)
        if c3.button("→ Park", key=f"park_{t['id']}", use_container_width=True):
            db.move_task(t["id"], "parking")
            st.rerun()


def _render_completed_tasks(tasks: list[dict]) -> None:
    if not tasks:
        return
    label = f"Completed · {len(tasks)}"
    with st.expander(label, expanded=False):
        for t in tasks:
            c1, c2 = st.columns([1, 8])
            still_done = c1.checkbox(
                "done",
                value=True,
                key=f"done_{t['id']}",
                label_visibility="collapsed",
            )
            if not still_done:
                db.set_done(t["id"], False)
                st.rerun()
            badge = _BADGE_HTML if _is_recurring(t) else ""
            c2.markdown(
                f"<span style='text-decoration:line-through;color:var(--text-muted)'>"
                f"{t['text']}</span>{badge}",
                unsafe_allow_html=True,
            )


def _render_parking_lot(tasks: list[dict]) -> None:
    label = f"Parking Lot · {len(tasks)} item{'s' if len(tasks) != 1 else ''}"
    with st.expander(label, expanded=False):
        if not tasks:
            st.caption("Parking lot is empty")
            return
        for t in tasks:
            c1, c2 = st.columns([6, 2])
            c1.markdown(t["text"])
            if c2.button("→ Today", key=f"promote_{t['id']}", use_container_width=True):
                db.move_task(t["id"], "today")
                st.rerun()


def render() -> None:
    open_today = db.get_open_today()
    completed_today = db.get_completed_today()
    parking = db.get_parking()

    _render_progress(len(open_today), len(completed_today))

    st.caption(f"TODAY · {len(open_today)} open")
    _render_open_tasks(open_today)
    _render_completed_tasks(completed_today)

    st.divider()
    _render_quick_add()

    st.divider()
    _render_parking_lot(parking)
