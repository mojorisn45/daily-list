from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class RolloverPlan:
    archive_ids: list[int] = field(default_factory=list)
    archive_date: date | None = None
    parking_ids: list[int] = field(default_factory=list)
    new_recurring_templates: list[dict] = field(default_factory=list)
    new_last_rollover: date | None = None

    @property
    def is_noop(self) -> bool:
        return self.new_last_rollover is None


def compute_rollover_plan(
    today: date,
    last_rollover: date | None,
    live_tasks: list[dict],
    templates: list[dict],
) -> RolloverPlan:
    if last_rollover is not None and last_rollover >= today:
        return RolloverPlan()

    archive_date = last_rollover if last_rollover is not None else today

    today_tasks = [t for t in live_tasks if t.get("list") == "today"]
    archive_ids = [t["id"] for t in today_tasks if t.get("done")]
    parking_ids = [t["id"] for t in today_tasks if not t.get("done")]

    return RolloverPlan(
        archive_ids=archive_ids,
        archive_date=archive_date,
        parking_ids=parking_ids,
        new_recurring_templates=list(templates),
        new_last_rollover=today,
    )


def apply_rollover_plan(plan: RolloverPlan) -> None:
    if plan.is_noop:
        return
    import db

    assert plan.archive_date is not None
    assert plan.new_last_rollover is not None
    db.bulk_archive(plan.archive_ids, plan.archive_date)
    db.bulk_move_to_parking(plan.parking_ids)
    db.bulk_insert_recurring_today(plan.new_recurring_templates)
    db.set_last_rollover_date(plan.new_last_rollover)


def run_rollover_if_needed() -> RolloverPlan:
    import streamlit as st
    import db

    today = db.today_local()

    if "dev_mode" in st.secrets and st.secrets["dev_mode"]:
        force = st.query_params.get("force_rollover")
        if force:
            today = date.fromisoformat(force)

    last = db.get_last_rollover_date()
    live = db.get_all_live_tasks()
    templates = db.get_recurring_templates()
    plan = compute_rollover_plan(today, last, live, templates)
    apply_rollover_plan(plan)
    return plan
