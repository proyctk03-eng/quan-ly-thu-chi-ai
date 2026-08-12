"""Unit tests for SQLite database operations and models."""

import os
import sqlite3
import pytest

DB_NAME = "test_chi_tieu.db"

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS giao_dich (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loai TEXT NOT NULL,
            so_tien REAL NOT NULL,
            danh_muc TEXT NOT NULL,
            ngay TEXT NOT NULL,
            ghi_chu TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS han_muc (
            danh_muc TEXT PRIMARY KEY,
            so_tien_limit REAL NOT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def test_insert_and_select_transaction(db_conn):
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
        ("Chi", 35000, "Ăn uống", "2026-08-12", "Cơm trưa phở")
    )
    db_conn.commit()
    
    cursor.execute("SELECT loai, so_tien, danh_muc FROM giao_dich WHERE id = 1")
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "Chi"
    assert row[1] == 35000
    assert row[2] == "Ăn uống"

def test_budget_limit_setting(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO han_muc (danh_muc, so_tien_limit) VALUES (?, ?)", ("Ăn uống", 2000000))
    db_conn.commit()
    
    cursor.execute("SELECT so_tien_limit FROM han_muc WHERE danh_muc = 'Ăn uống'")
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == 2000000
