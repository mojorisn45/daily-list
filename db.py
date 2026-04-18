from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st
from supabase import Client, create_client

TZ = ZoneInfo("America/Chicago")


@st.cache_resource
def get_client() -> Client:
    return create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])


def now_local() -> datetime:
    return datetime.now(TZ)


def today_local() -> date:
    return now_local().date()


# ---------- Reads ----------

def get_open_today() -> list[dict]:
    res = (
        get_client().table("tasks").select("*")
        .eq("archived", False).eq("list", "today").eq("done", False)
        .order("created_at", desc=True).execute()
    )
    return res.data or []


def get_completed_today() -> list[dict]:
    res = (
        get_client().table("tasks").select("*")
        .eq("archived", False).eq("list", "today").eq("done", True)
        .order("completed_at", desc=True).execute()
    )
    return res.data or []


def get_parking() -> list[dict]:
    res = (
        get_client().table("tasks").select("*")
        .eq("archived", False).eq("list", "parking")
        .order("created_at", desc=True).execute()
    )
    return res.data or []


def get_all_live_tasks() -> list[dict]:
    res = (
        get_client().table("tasks").select("*")
        .eq("archived", False).execute()
    )
    return res.data or []


def get_archive(days: int = 30) -> list[dict]:
    cutoff = (today_local() - timedelta(days=days)).isoformat()
    res = (
        get_client().table("tasks").select("*")
        .eq("archived", True).gte("archived_date", cutoff)
        .order("archived_date", desc=True)
        .order("completed_at", desc=True)
        .execute()
    )
    return res.data or []


def get_recurring_templates() -> list[dict]:
    res = (
        get_client().table("recurring_templates").select("*")
        .eq("active", True)
        .order("created_at", desc=False).execute()
    )
    return res.data or []


def get_last_rollover_date() -> date | None:
    res = (
        get_client().table("app_state").select("value")
        .eq("key", "last_rollover_date").maybe_single().execute()
    )
    if res is None or res.data is None:
        return None
    return date.fromisoformat(res.data["value"])


# ---------- Writes ----------

def add_task(text: str, list_name: str, recurring_id: int | None = None) -> dict:
    payload: dict = {"text": text, "list": list_name, "done": False}
    if recurring_id is not None:
        payload["recurring_id"] = recurring_id
    res = get_client().table("tasks").insert(payload).execute()
    return res.data[0] if res.data else {}


def set_done(task_id: int, done: bool) -> None:
    payload: dict = {"done": done, "completed_at": now_local().isoformat() if done else None}
    get_client().table("tasks").update(payload).eq("id", task_id).execute()


def move_task(task_id: int, new_list: str) -> None:
    get_client().table("tasks").update(
        {"list": new_list, "done": False, "completed_at": None}
    ).eq("id", task_id).execute()


def bulk_archive(task_ids: list[int], archived_date: date) -> None:
    if not task_ids:
        return
    get_client().table("tasks").update(
        {"archived": True, "archived_date": archived_date.isoformat()}
    ).in_("id", task_ids).execute()


def bulk_move_to_parking(task_ids: list[int]) -> None:
    if not task_ids:
        return
    get_client().table("tasks").update(
        {"list": "parking", "done": False, "completed_at": None}
    ).in_("id", task_ids).execute()


def bulk_insert_recurring_today(templates: list[dict]) -> None:
    if not templates:
        return
    rows = [
        {"text": t["text"], "list": "today", "done": False, "recurring_id": t["id"]}
        for t in templates
    ]
    get_client().table("tasks").insert(rows).execute()


def add_recurring(text: str) -> dict:
    res = (
        get_client().table("recurring_templates")
        .insert({"text": text, "active": True}).execute()
    )
    return res.data[0] if res.data else {}


def remove_recurring(template_id: int) -> None:
    get_client().table("recurring_templates").update(
        {"active": False}
    ).eq("id", template_id).execute()


def set_last_rollover_date(d: date) -> None:
    get_client().table("app_state").upsert(
        {"key": "last_rollover_date", "value": d.isoformat()}
    ).execute()
