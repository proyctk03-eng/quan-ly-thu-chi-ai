"""Transaction CRUD service — pure database logic, no Streamlit."""

from __future__ import annotations

from typing import Any

from backend.core.database import get_db_connection


def list_transactions(
    keyword: str | None = None,
    category: str | None = None,
    month: str | None = None,
) -> list[dict[str, Any]]:
    """Return transactions with optional filters."""
    conn = get_db_connection()
    query = (
        "SELECT id, loai, so_tien, danh_muc, ngay, ghi_chu "
        "FROM giao_dich ORDER BY ngay DESC, id DESC"
    )
    rows = conn.execute(query).fetchall()
    conn.close()

    results = [dict(r) for r in rows]

    if keyword:
        kw = keyword.lower()
        results = [
            r for r in results
            if kw in (r.get("ghi_chu") or "").lower()
            or kw in (r.get("danh_muc") or "").lower()
        ]
    if category:
        results = [r for r in results if r["danh_muc"] == category]
    if month:
        results = [r for r in results if r["ngay"][:7] == month]

    return results


def get_transaction(transaction_id: int) -> dict[str, Any] | None:
    """Return a single transaction by ID, or *None*."""
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, loai, so_tien, danh_muc, ngay, ghi_chu "
        "FROM giao_dich WHERE id = ?",
        (transaction_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def add_transaction(
    loai: str,
    so_tien: float,
    danh_muc: str,
    ngay: str,
    ghi_chu: str = "",
) -> int:
    """Insert a new transaction and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) "
        "VALUES (?, ?, ?, ?, ?)",
        (loai, so_tien, danh_muc, ngay, ghi_chu),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id  # type: ignore[return-value]


def update_transaction(
    transaction_id: int,
    loai: str,
    so_tien: float,
    danh_muc: str,
    ngay: str,
    ghi_chu: str = "",
) -> bool:
    """Update a transaction; return *True* on success."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE giao_dich "
        "SET loai = ?, so_tien = ?, danh_muc = ?, ngay = ?, ghi_chu = ? "
        "WHERE id = ?",
        (loai, so_tien, danh_muc, ngay, ghi_chu, transaction_id),
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_transaction(transaction_id: int) -> bool:
    """Delete a transaction; return *True* on success."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM giao_dich WHERE id = ?", (transaction_id,)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def bulk_import_transactions(
    rows: list[dict[str, Any]],
) -> int:
    """Insert many transactions from a list of dicts; return count."""
    conn = get_db_connection()
    cursor = conn.cursor()
    count = 0
    for row in rows:
        cursor.execute(
            "INSERT INTO giao_dich "
            "(loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
            (
                str(row["loai"]),
                float(row["so_tien"]),
                str(row["danh_muc"]),
                str(row["ngay"]),
                str(row.get("ghi_chu", "")),
            ),
        )
        count += 1
    conn.commit()
    conn.close()
    return count
