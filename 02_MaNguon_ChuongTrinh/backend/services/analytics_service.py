"""Analytics service — financial summaries and monthly comparisons."""

from __future__ import annotations

import datetime

from backend.core.database import get_db_connection


def get_financial_summary() -> dict[str, float]:
    """Return ``{tong_thu, tong_chi, so_du}``."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            SUM(CASE WHEN loai = 'Thu' THEN so_tien ELSE 0 END) AS tong_thu,
            SUM(CASE WHEN loai = 'Chi' THEN so_tien ELSE 0 END) AS tong_chi
        FROM giao_dich
    """)
    row = cursor.fetchone()
    conn.close()

    tong_thu = row["tong_thu"] if row and row["tong_thu"] else 0.0
    tong_chi = row["tong_chi"] if row and row["tong_chi"] else 0.0
    return {
        "tong_thu": tong_thu,
        "tong_chi": tong_chi,
        "so_du": tong_thu - tong_chi,
    }


def get_monthly_comparison() -> dict:
    """Compare spending / income of the current month vs previous month."""
    conn = get_db_connection()
    today = datetime.date.today()
    current_m = today.strftime("%Y-%m")
    prev_m = (today.replace(day=1) - datetime.timedelta(days=1)).strftime(
        "%Y-%m"
    )

    def _sum_by(loai: str, month: str) -> float:
        row = conn.execute(
            "SELECT COALESCE(SUM(so_tien), 0) AS total "
            "FROM giao_dich "
            "WHERE loai = ? AND substr(ngay, 1, 7) = ?",
            (loai, month),
        ).fetchone()
        return float(row["total"]) if row else 0.0

    chi_this = _sum_by("Chi", current_m)
    chi_prev = _sum_by("Chi", prev_m)
    thu_this = _sum_by("Thu", current_m)
    thu_prev = _sum_by("Thu", prev_m)
    conn.close()

    chi_delta = chi_this - chi_prev
    thu_delta = thu_this - thu_prev

    return {
        "current_month": current_m,
        "chi_this": chi_this,
        "chi_prev": chi_prev,
        "chi_delta": chi_delta,
        "chi_delta_pct": (
            f"{chi_delta / chi_prev * 100:+.1f}%"
            if chi_prev > 0
            else "N/A"
        ),
        "thu_this": thu_this,
        "thu_prev": thu_prev,
        "thu_delta": thu_delta,
        "thu_delta_pct": (
            f"{thu_delta / thu_prev * 100:+.1f}%"
            if thu_prev > 0
            else "N/A"
        ),
    }
