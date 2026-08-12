# SCREEN FLOW & TÀI LIỆU THIẾT KẾ CƠ SỞ DỮ LIỆU

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 01 - CNTT K23K  

---

## 1. Sơ Đồ Phân Luồng Màn Hình (Screen Flow)

```
[Màn hình Chính Streamlit Web App]
   ├── Tab 1: 📊 Thống Kê & Ngân Sách (Metric cards, Progress bars, Chart Pie/Bar/Line)
   ├── Tab 2: ➕ Thêm Chi Tiêu (AI Natural Language Input + Form Thủ Công)
   ├── Tab 3: 📜 Lịch Sử (Danh sách Dataframe, Bộ lọc 3 tiêu chí, Edit/Delete confirm 2-step, Export/Import)
   ├── Tab 4: 🧠 Gợi Ý Tiết Kiệm (Gemini Advice Generator)
   ├── Tab 5: 🤖 Trợ Lý Gemini (Chatbot Finance & Math QA)
   └── Floating Widget: 💬 CSKH AI Popover Nổi góc dưới bên phải màn hình
```

## 2. Cấu Trúc Cơ Sở Dữ Liệu SQLite (`chi_tieu.db`)

### Bảng 1: `giao_dich` (Lưu lịch sử thu chi)
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT): Mã giao dịch.
- `loai` (TEXT NOT NULL): 'Thu' hoặc 'Chi'.
- `so_tien` (REAL NOT NULL): Số tiền VNĐ (> 0).
- `danh_muc` (TEXT NOT NULL): 1 trong 9 danh mục sinh viên.
- `ngay` (TEXT NOT NULL): Định dạng YYYY-MM-DD.
- `ghi_chu` (TEXT): Mô tả giao dịch.
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP): Thời gian tạo.

### Bảng 2: `han_muc` (Lưu hạn mức chi tiêu tháng)
- `danh_muc` (TEXT PRIMARY KEY): Tên danh mục.
- `so_tien_limit` (REAL NOT NULL): Số tiền hạn mức tối đa.
