"""Budget-limit service — pure database logic."""

from __future__ import annotations

from typing import Any

from backend.core.database import get_db_connection


def get_budget_limits() -> dict[str, float]:
    """Return all budget limits as ``{category: limit}``."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT danh_muc, so_tien_limit FROM han_muc"
    ).fetchall()
    conn.close()
    return {r["danh_muc"]: r["so_tien_limit"] for r in rows}


def set_budget_limit(danh_muc: str, so_tien_limit: float) -> None:
    """Insert or replace a budget limit for *danh_muc*."""
    conn = get_db_connection()
    conn.execute(
        "INSERT OR REPLACE INTO han_muc "
        "(danh_muc, so_tien_limit) VALUES (?, ?)",
        (danh_muc, so_tien_limit),
    )
    conn.commit()
    conn.close()


def get_all_limits_list() -> list[dict[str, Any]]:
    """Return budget limits as a list of dicts."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT danh_muc, so_tien_limit FROM han_muc"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
