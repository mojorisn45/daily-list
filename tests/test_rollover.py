from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rollover import RolloverPlan, compute_rollover_plan


def _task(id: int, list_: str, done: bool, recurring_id: int | None = None) -> dict:
    return {"id": id, "list": list_, "done": done, "recurring_id": recurring_id}


def test_noop_same_day():
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 18), [], [])
    assert plan.is_noop
    assert plan == RolloverPlan()


def test_noop_future_last_defensive():
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 20), [], [])
    assert plan.is_noop


def test_single_day_rollover_partitions_today_tasks():
    tasks = [
        _task(1, "today", True),
        _task(2, "today", True),
        _task(3, "today", False),
        _task(4, "today", False),
    ]
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 17), tasks, [])
    assert set(plan.archive_ids) == {1, 2}
    assert set(plan.parking_ids) == {3, 4}
    assert plan.archive_date == date(2026, 4, 17)
    assert plan.new_last_rollover == date(2026, 4, 18)


def test_parking_tasks_never_touched():
    tasks = [
        _task(1, "today", True),
        _task(2, "parking", False),
        _task(3, "parking", True),  # shouldn't happen but defend
    ]
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 17), tasks, [])
    assert plan.archive_ids == [1]
    assert plan.parking_ids == []


def test_multi_day_gap_does_not_backfill_recurring():
    templates = [{"id": 1, "text": "A"}, {"id": 2, "text": "B"}]
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 13), [], templates)
    assert len(plan.new_recurring_templates) == 2
    assert plan.new_last_rollover == date(2026, 4, 18)
    assert plan.archive_date == date(2026, 4, 13)


def test_multi_day_gap_still_archives_and_parks_once():
    tasks = [_task(1, "today", True), _task(2, "today", False)]
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 10), tasks, [])
    assert plan.archive_ids == [1]
    assert plan.parking_ids == [2]
    assert plan.archive_date == date(2026, 4, 10)


def test_no_recurring_templates():
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 17), [], [])
    assert plan.new_recurring_templates == []
    assert not plan.is_noop


def test_recurring_templates_copied_into_plan():
    templates = [{"id": 7, "text": "Morning journal"}]
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 17), [], templates)
    assert plan.new_recurring_templates == templates


def test_none_last_rollover_runs_with_today_as_archive_date():
    plan = compute_rollover_plan(date(2026, 4, 18), None, [], [])
    assert not plan.is_noop
    assert plan.new_last_rollover == date(2026, 4, 18)
    assert plan.archive_date == date(2026, 4, 18)


def test_all_completed_today():
    tasks = [_task(i, "today", True) for i in range(1, 6)]
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 17), tasks, [])
    assert set(plan.archive_ids) == {1, 2, 3, 4, 5}
    assert plan.parking_ids == []


def test_empty_live_tasks():
    plan = compute_rollover_plan(date(2026, 4, 18), date(2026, 4, 17), [], [])
    assert plan.archive_ids == []
    assert plan.parking_ids == []
    assert not plan.is_noop


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(failed)
