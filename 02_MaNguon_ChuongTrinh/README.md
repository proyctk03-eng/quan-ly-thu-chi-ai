# 🎓 Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI

Ứng dụng web thông minh giúp sinh viên quản lý tài chính cá nhân, được xây dựng bằng **Python**, **Streamlit**, **Plotly** và tích hợp **Google Gemini AI**.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Cấu hình API Key
```bash
# Copy file mẫu và điền API Key của bạn
cp .env.example .env
# Mở file .env và thay thế "your_gemini_api_key_here" bằng API Key thật
```

> 💡 **Lấy API Key miễn phí tại**: [Google AI Studio](https://aistudio.google.com/)

### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trình duyệt tại `http://localhost:8502`

---

## ✨ Tính Năng Chính

### 📊 1. Dashboard Thống Kê Trực Quan
- **3 thẻ chỉ số**: Tổng Thu, Tổng Chi, Số Dư Ví với cảnh báo cháy túi tự động
- **Hạn mức ngân sách**: Thiết lập và theo dõi giới hạn chi tiêu theo danh mục
- **Biểu đồ Plotly**: Pie Chart phân bổ chi tiêu & Bar Chart Thu vs Chi theo tháng
- **Giao diện thích ứng**: Tự động đồng bộ Light/Dark mode

### ➕ 2. Nhập Chi Tiêu Nhanh Bằng AI
- **Nhập bằng ngôn ngữ tự nhiên**: Gõ "ăn phở 35k", "bố mẹ gửi 4 triệu" → AI tự phân tích
- **Structured Outputs**: Đảm bảo 100% JSON hợp lệ nhờ `response_schema`
- **Mapping danh mục thông minh**: AI tự ánh xạ vào danh mục chuẩn của CSDL
- **Form nhập thủ công**: Backup khi không muốn dùng AI

### 📜 3. Lịch Sử & Quản Lý Giao Dịch
- **Tìm kiếm & Lọc**: Theo từ khóa, danh mục, tháng
- **Sửa & Xóa**: Chỉnh sửa/xóa trực tiếp trên giao diện
- **Xuất báo cáo**: CSV và Excel (.xlsx)
- **Nhập dữ liệu**: Upload file CSV để import hàng loạt

### 🧠 4. Tư Vấn Tiết Kiệm AI
- Gemini AI phân tích dữ liệu chi tiêu thực tế của bạn
- Đưa ra lời khuyên tiết kiệm cá nhân hóa cho sinh viên

### 🤖 5. Trợ Lý Chatbot AI
- Hỏi đáp trực tiếp về tài chính & toán học
- Tích hợp dữ liệu ví hiện tại để trả lời chính xác
- Từ chối nghiêm ngặt các câu hỏi ngoài chuyên môn

---

## 🏗️ Cấu Trúc Dự Án

```
quan_ly_thu_chi/
├── .env                    # API Key (không commit lên Git)
├── .env.example            # Mẫu cấu hình biến môi trường
├── .gitignore              # Danh sách file bỏ qua khi commit
├── .streamlit/
│   └── config.toml         # Cấu hình theme & server Streamlit
├── app.py                  # Mã nguồn chính của ứng dụng
├── agent_test.py           # Script test Google Antigravity Agent
├── test_main.py            # Kịch bản kiểm thử pytest
├── requirements.txt        # Danh sách thư viện phụ thuộc
├── chi_tieu.db             # CSDL SQLite (tự động tạo khi chạy)
└── README.md               # Tài liệu hướng dẫn (file này)
```

---

## 🔧 Công Nghệ Sử Dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Frontend   | Streamlit, Custom CSS (Light/Dark adaptive) |
| Biểu đồ   | Plotly Express |
| CSDL       | SQLite3 |
| AI Engine  | Google Gemini 3.5 Flash (Structured Outputs) |
| Agent      | Google Antigravity SDK |
| Bảo mật    | python-dotenv + st.secrets fallback |

---

## 📝 Ghi Chú

- **API Key Free Tier**: Giới hạn 5 requests/phút và 20 requests/ngày. Nếu gặp lỗi `429 RESOURCE_EXHAUSTED`, vui lòng đợi 1 phút hoặc nâng cấp gói.
- **CSDL**: File `chi_tieu.db` được tự động tạo khi lần đầu chạy ứng dụng với dữ liệu mẫu sinh viên.
