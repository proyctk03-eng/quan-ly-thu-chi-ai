# HƯỚNG DẪN SỬ DỤNG VÀ TRIỂN KHAI DỰ ÁN

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 01 - CNTT K23K  

---

## 1. Triển Khai Nhanh Bằng Docker Compose (Khuyên Dùng)

```bash
# 1. Clone hoặc tải mã nguồn dự án
cd quan_ly_thu_chi

# 2. Khởi động Docker Compose
docker-compose up --build
```

- **Frontend Streamlit UI**: [http://localhost:8502](http://localhost:8502)
- **Backend FastAPI Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 2. Triển Khai Thủ Công Cục Bộ (Local Python)

```bash
# Terminal 1: Chạy Backend FastAPI
uvicorn backend.main:app --reload --port 8000

# Terminal 2: Chạy Frontend Streamlit
python -m streamlit run frontend/app.py --server.port 8502
```

---

## 3. Hướng Dẫn Sử Dụng Chi Tiết

1. **Tab 📊 Thống Kê**: Xem tổng thu chi, số dư ví, sức khỏe tài chính, so sánh tháng này vs tháng trước và 3 biểu đồ Plotly (Pie, Bar, Line trend).
2. **Tab ➕ Thêm Chi Tiêu**: Gõ câu tự nhiên (VD: "Sáng ăn phở 35k", "Chiều tiêu 5 củ"), Gemini AI tự động bóc tách số tiền, cảnh báo ví và đưa nút xác nhận lưu vào sổ.
3. **Tab 📜 Lịch Sử**: Lọc theo từ khóa/danh mục/tháng, sửa giao dịch, xóa với xác nhận 2 bước, xuất báo cáo CSV/Excel.
4. **Tab 🧠 Gợi Ý Tiết Kiệm**: Nhấn nút phân tích để Gemini AI xuất lời khuyên tài chính cá nhân hóa.
5. **Tab 🤖 Trợ Lý Gemini**: Hỏi đáp kiến thức tài chính & hỗ trợ giải bài tập toán học.
6. **Widget CSKH Nổi 💬**: Nhấp vào biểu tượng chat góc dưới bên phải để ra lệnh trực tiếp bằng ngôn ngữ tự nhiên.
