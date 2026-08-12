"""SQLite database engine: connection factory and schema initialisation."""

import datetime
import sqlite3

from backend.core.config import DB_FILE


def get_db_connection() -> sqlite3.Connection:
    """Create and return a new SQLite connection with ``Row`` factory."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables and seed sample data when the database is empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Transactions table
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

    # Budget limits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS han_muc (
            danh_muc TEXT PRIMARY KEY,
            so_tien_limit REAL NOT NULL
        )
    """)
    conn.commit()

    # Seed sample data for students
    cursor.execute("SELECT COUNT(*) FROM giao_dich")
    if cursor.fetchone()[0] == 0:
        today = datetime.date.today()
        sample_transactions = [
            ("Thu", 4000000, "Chu cấp gia đình",
             today.strftime("%Y-%m-01"), "Bố mẹ gửi tiền tháng này 💰"),
            ("Thu", 2500000, "Đi làm thêm",
             today.strftime("%Y-%m-05"), "Lương gia sư / quán cafe 💼"),
            ("Chi", 1800000, "Tiền nhà & Tiện ích",
             today.strftime("%Y-%m-02"), "Tiền phòng trọ & điện nước 🏠"),
            ("Chi", 1500000, "Ăn uống & Cafe",
             today.strftime("%Y-%m-03"),
             "Cơm tháng, ăn vặt & cafe chạy deadline 🍜"),
            ("Chi", 450000, "Học tập & Sách vở",
             today.strftime("%Y-%m-04"), "In giáo trình & mua tài liệu học 📚"),
            ("Chi", 300000, "Di chuyển & Xăng xe",
             today.strftime("%Y-%m-06"), "Đổ xăng & vé xe bus 🛵"),
            ("Chi", 350000, "Giải trí & Bè bạn",
             today.strftime("%Y-%m-07"),
             "Xem phim & ăn đồ nướng cuối tuần 🎬"),
        ]
        cursor.executemany(
            "INSERT INTO giao_dich "
            "(loai, so_tien, danh_muc, ngay, ghi_chu) "
            "VALUES (?, ?, ?, ?, ?)",
            sample_transactions,
        )

        sample_limits = [
            ("Ăn uống & Cafe", 2500000),
            ("Tiền nhà & Tiện ích", 2000000),
            ("Giải trí & Bè bạn", 800000),
            ("Học tập & Sách vở", 600000),
            ("Di chuyển & Xăng xe", 500000),
        ]
        cursor.executemany(
            "INSERT OR REPLACE INTO han_muc "
            "(danh_muc, so_tien_limit) VALUES (?, ?)",
            sample_limits,
        )
        conn.commit()
    conn.close()
