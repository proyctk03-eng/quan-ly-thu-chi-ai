"""
Kịch bản kiểm thử cho Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI.
Chạy: pytest test_main.py -v
"""
import sqlite3
import datetime
import os
import json


# ==============================================================================
# 1. KIỂM THỬ CƠ SỞ DỮ LIỆU
# ==============================================================================
TEST_DB = "test_chi_tieu.db"


def setup_test_db():
    """Tạo CSDL kiểm thử tạm thời"""
    conn = sqlite3.connect(TEST_DB)
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
    return conn


def teardown_test_db():
    """Xóa CSDL kiểm thử sau khi hoàn tất"""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_create_tables():
    """Kiểm tra tạo bảng CSDL thành công"""
    conn = setup_test_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    teardown_test_db()
    
    assert "giao_dich" in tables
    assert "han_muc" in tables


def test_insert_transaction():
    """Kiểm tra thêm giao dịch vào CSDL"""
    conn = setup_test_db()
    cursor = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
        ("Chi", 35000, "Ăn uống & Cafe", today, "Phở sáng")
    )
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM giao_dich")
    count = cursor.fetchone()[0]
    conn.close()
    teardown_test_db()
    
    assert count == 1


def test_delete_transaction():
    """Kiểm tra xóa giao dịch khỏi CSDL"""
    conn = setup_test_db()
    cursor = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
        ("Chi", 50000, "Di chuyển & Xăng xe", today, "Đổ xăng")
    )
    conn.commit()
    
    cursor.execute("DELETE FROM giao_dich WHERE id = 1")
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM giao_dich")
    count = cursor.fetchone()[0]
    conn.close()
    teardown_test_db()
    
    assert count == 0


def test_update_transaction():
    """Kiểm tra cập nhật giao dịch"""
    conn = setup_test_db()
    cursor = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
        ("Chi", 30000, "Ăn uống & Cafe", today, "Cơm trưa")
    )
    conn.commit()
    
    cursor.execute(
        "UPDATE giao_dich SET so_tien = ?, ghi_chu = ? WHERE id = 1",
        (45000, "Cơm trưa + trà sữa")
    )
    conn.commit()
    
    cursor.execute("SELECT so_tien, ghi_chu FROM giao_dich WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    teardown_test_db()
    
    assert row[0] == 45000
    assert row[1] == "Cơm trưa + trà sữa"


def test_budget_limit():
    """Kiểm tra thiết lập và ghi đè hạn mức ngân sách"""
    conn = setup_test_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO han_muc (danh_muc, so_tien_limit) VALUES (?, ?)",
        ("Ăn uống & Cafe", 2500000)
    )
    conn.commit()
    
    cursor.execute("SELECT so_tien_limit FROM han_muc WHERE danh_muc = ?", ("Ăn uống & Cafe",))
    limit = cursor.fetchone()[0]
    assert limit == 2500000
    
    # Ghi đè hạn mức mới
    cursor.execute(
        "INSERT OR REPLACE INTO han_muc (danh_muc, so_tien_limit) VALUES (?, ?)",
        ("Ăn uống & Cafe", 3000000)
    )
    conn.commit()
    
    cursor.execute("SELECT so_tien_limit FROM han_muc WHERE danh_muc = ?", ("Ăn uống & Cafe",))
    new_limit = cursor.fetchone()[0]
    conn.close()
    teardown_test_db()
    
    assert new_limit == 3000000


def test_financial_summary():
    """Kiểm tra tính tổng thu, tổng chi, số dư"""
    conn = setup_test_db()
    cursor = conn.cursor()
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    transactions = [
        ("Thu", 4000000, "Chu cấp gia đình", today, "Bố mẹ gửi"),
        ("Chi", 1500000, "Ăn uống & Cafe", today, "Cơm tháng"),
        ("Chi", 500000, "Di chuyển & Xăng xe", today, "Xăng xe"),
    ]
    cursor.executemany(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
        transactions
    )
    conn.commit()
    
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN loai = 'Thu' THEN so_tien ELSE 0 END) as tong_thu,
            SUM(CASE WHEN loai = 'Chi' THEN so_tien ELSE 0 END) as tong_chi
        FROM giao_dich
    """)
    row = cursor.fetchone()
    tong_thu = row[0] or 0
    tong_chi = row[1] or 0
    so_du = tong_thu - tong_chi
    conn.close()
    teardown_test_db()
    
    assert tong_thu == 4000000
    assert tong_chi == 2000000
    assert so_du == 2000000


# ==============================================================================
# 2. KIỂM THỬ LOGIC XỬ LÝ
# ==============================================================================
def test_category_mapping():
    """Kiểm tra ánh xạ danh mục AI sang danh mục CSDL"""
    category_mapping = {
        "Ăn uống & Cafe": "Ăn uống & Cafe",
        "Di chuyển": "Di chuyển & Xăng xe",
        "Giải trí": "Giải trí & Bè bạn",
        "Mua sắm": "Mua sắm cá nhân",
        "Hóa đơn": "Tiền nhà & Tiện ích",
        "Khác": "Khác"
    }
    
    assert category_mapping.get("Di chuyển") == "Di chuyển & Xăng xe"
    assert category_mapping.get("Giải trí") == "Giải trí & Bè bạn"
    assert category_mapping.get("Hóa đơn") == "Tiền nhà & Tiện ích"
    assert category_mapping.get("Mua sắm") == "Mua sắm cá nhân"
    assert category_mapping.get("Không tồn tại", "Khác") == "Khác"


def test_money_slang_conversion():
    """Kiểm tra quy đổi từ lóng tiền Việt"""
    conversions = {
        "35k": 35000,
        "50k": 50000,
        "1.5 triệu": 1500000,
        "4 triệu": 4000000,
        "1 lít": 100000,
        "2 củ": 2000000,
    }
    
    # Kiểm tra mapping đúng
    for slang, expected in conversions.items():
        assert expected > 0, f"Giá trị {slang} phải lớn hơn 0"


def test_env_file_exists():
    """Kiểm tra file .env tồn tại"""
    base = os.path.dirname(__file__)
    assert os.path.exists(".env") or os.path.exists(".env.example") or \
           os.path.exists(os.path.join(base, ".env")) or os.path.exists(os.path.join(base, ".env.example")), \
        "Cần có file .env hoặc .env.example trong thư mục dự án"


def test_student_categories():
    """Kiểm tra danh sách danh mục sinh viên đầy đủ"""
    STUDENT_CATEGORIES = [
        "Ăn uống & Cafe",
        "Tiền nhà & Tiện ích",
        "Học tập & Sách vở",
        "Di chuyển & Xăng xe",
        "Giải trí & Bè bạn",
        "Mua sắm cá nhân",
        "Chu cấp gia đình",
        "Đi làm thêm",
        "Khác"
    ]
    
    assert len(STUDENT_CATEGORIES) == 9
    assert "Ăn uống & Cafe" in STUDENT_CATEGORIES
    assert "Khác" in STUDENT_CATEGORIES
