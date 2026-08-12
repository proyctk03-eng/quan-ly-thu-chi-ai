"""
Script tự động sinh 7 bộ tài liệu báo cáo dự án SDLC chuẩn cho:
Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIRS = [
    r"C:\Users\Admin\.gemini\antigravity-ide\scratch\quan_ly_thu_chi\drive-download-20260812T125606Z-1-001\CacGiaiDoanThucHien",
    r"C:\Users\Admin\.gemini\antigravity-ide\scratch\quan_ly_thu_chi\drive-download-20260812T125606Z-1-001\Mau"
]

print("Starting generation script setup...")
