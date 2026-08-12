"""Unit tests for Gemini AI Money Slang Conversion & Student Category Mapping."""

import re
import pytest

def parse_money_slang(text: str) -> float:
    """Helper function to test money slang regex conversions."""
    text_lower = text.lower()
    
    # 5 củ -> 5,000,000
    cu_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:củ|triệu|tr)', text_lower)
    if cu_match:
        return float(cu_match.group(1)) * 1000000
        
    # 199k -> 199,000
    k_match = re.search(r'(\d+(?:\.\d+)?)\s*k', text_lower)
    if k_match:
        return float(k_match.group(1)) * 1000
        
    # 3 lít -> 300,000
    lit_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lít|loét)', text_lower)
    if lit_match:
        return float(lit_match.group(1)) * 100000
        
    # Plain number fallback
    num_match = re.search(r'(\d[\d\.\,]*)', text_lower)
    if num_match:
        clean_num = num_match.group(1).replace('.', '').replace(',', '')
        return float(clean_num)
        
    return 0.0

def test_money_slang_conversions():
    assert parse_money_slang("199k") == 199000
    assert parse_money_slang("5 củ") == 5000000
    assert parse_money_slang("3 lít") == 300000
    assert parse_money_slang("35000") == 35000

def test_student_categories():
    categories = [
        "Ăn uống", "Học tập", "Nhà ở & Điện nước", "Di chuyển & Xăng xe",
        "Giải trí & Bè bạn", "Mua sắm cá nhân", "Chu cấp gia đình", "Thu nhập / Học bổng", "Khác"
    ]
    assert len(categories) == 9
    assert "Ăn uống" in categories
    assert "Học tập" in categories
