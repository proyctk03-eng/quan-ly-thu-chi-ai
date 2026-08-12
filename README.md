<div align="center">

# 🎓 Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI
### Modern SaaS Personal Finance & Smart Budgeting System for Students

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash--AI-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pytest](https://img.shields.io/badge/Tests-10%2F10%20PASS-brightgreen.svg?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

**Một hệ thống quản lý tài chính cá nhân thông minh, tích hợp Trợ lý AI Google Gemini, giúp sinh viên kiểm soát thu chi, lập hạn mức ngân sách và phòng tránh nguy cơ "cháy túi" cuối tháng.**

[🌐 Live Demo App](https://passive-couple-takes-composite.trycloudflare.com) • [📦 GitHub Repo](https://github.com/proyctk03-eng/quan-ly-thu-chi-ai) • [📄 Báo Cáo Đồ Án](./01_BaoCao_TàiLieu_Va_SoDo/)

</div>

---

## 📖 Bảng Mục Lục
- [🌟 Giới Thiệu Dự Án](#-giới-thiệu-dự-án)
- [✨ Tính Năng Nổi Bật](#-tính-năng-nổi-bật)
- [🎨 Thiết Kế UI/UX Chuẩn SaaS](#-thiết-kế-uiux-chuẩn-saas)
- [🏗️ Động Cơ AI & Xử Lý Ngôn Ngữ Tự Nhiên](#️-động-cơ-ai--xử-lý-ngôn-ngữ-tự-nhiên)
- [🚀 Hướng Dẫn Cài Đặt & Khởi Chạy](#-hướng-dẫn-cài-đặt--khởi-chạy)
- [🐳 Triển Khai Với Docker](#-triển-khai-với-docker)
- [🧪 Kiểm Thử Tự Động (Automated Testing)](#-kiểm-thử-tự-động-automated-testing)
- [📂 Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [👥 Nhóm Thực Hiện](#-nhóm-thực-hiện)

---

## 🌟 Giới Thiệu Dự Án

**Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI** được phát triển nhằm giải quyết bài toán quản lý tài chính cá nhân thường gặp ở sinh viên: chi tiêu thiếu kiểm soát, quên ghi chép nhật ký thu chi và thiếu lời khuyên tiết kiệm thực tế.

Ứng dụng kết hợp sức mạnh của **Streamlit** (Giao diện web phản hồi nhanh), **SQLite** (Cơ sở dữ liệu nhẹ, bền vững) và **Google Gemini AI** (Phân tích ngôn ngữ tự nhiên NLP & Structured Outputs).

---

## ✨ Tính Năng Nổi Bật

### 📊 1. Thống Kê & Phân Tích Trực Quan (Analytics Dashboard)
- **Tổng quan thu chi**: Theo dõi Số Dư Ví, Tổng Thu Nhập, Tổng Chi Tiêu với cảnh báo báo động tự động (`Báo động hết tiền!` / `Cháy túi!`).
- **Phân tích so sánh**: So sánh tăng/giảm thu chi so với tháng trước theo tỷ lệ phần trăm (%).
- **Thẻ Hạn Mức Tiêu Tháng**: Đóng khung công nghệ (Tech Card) hiển thị tiến độ tiêu xài theo từng danh mục (Ăn uống, Nhà ở, Học tập, Giải trí...) với thanh Progress Bar dải màu Gradient.
- **Biểu đồ tương tác (Plotly Express)**:
  - *Pie Chart*: Phân bổ tỷ lệ % các khoản chi chiếm nhiều tiền nhất.
  - *Grouped Bar Chart*: So sánh tương quan tổng Thu vs tổng Chi theo từng tháng.
  - *Line Trend Chart*: Xu hướng chi tiêu tích lũy theo từng ngày trong tháng.

### ➕ 2. Nhập Chi Tiêu Nhanh Bằng Ngôn Ngữ Tự Nhiên (AI Transaction Parser)
- Gõ các câu thông thường như:
  - *"Sáng ăn phở 35k, chiều mua sách 120k"*
  - *"Bố mẹ cho 3 triệu tiền nhà"*
  - *"Vừa tiêu 5 củ đóng tiền trọ"*
- AI tự động trích xuất thông tin: **Loại (Thu/Chi)**, **Số tiền (VND - chuyển đổi slang 'k', 'củ', 'm' chuẩn xác)**, **Danh mục sinh viên** và **Ghi chú**.

### 📜 3. Lịch Sử & Quản Lý Giao Dịch
- **Bộ lọc đa năng**: Tìm kiếm theo từ khóa ghi chú, lọc danh mục và lọc theo tháng.
- **Quản lý dữ liệu**: Hỗ trợ Chỉnh sửa (Edit) và Xóa (Delete) trực tiếp với hộp thoại xác nhận an toàn.
- **Xuất / Nhập báo cáo**: Tải file báo cáo dạng **CSV** hoặc **Excel (.xlsx)**; hỗ trợ Nhập dữ liệu hàng loạt từ file CSV.

### 🧠 4. AI Tư Vấn Tiết Kiệm Cá Nhân Hóa
- Google Gemini AI phân tích hành vi tài chính thực tế trong CSDL và đưa ra chiến lược tiết kiệm chi tiết dành riêng cho sinh viên.

### 🤖 5. Trợ Lý Tài Chính Sinh Viên Floating Card (Floating Action Button - FAB)
- Nút bấm tròn nổi `🤖` ghim cố định ở góc dưới bên phải màn hình.
- Cho phép trò chuyện trực tiếp với AI Assistant, thực thi các lệnh quản lý tài chính nhanh gọn ở bất kỳ Tab nào.

---

## 🎨 Thiết Kế UI/UX Chuẩn SaaS

- **Giao diện Segmented Control Tabs**: Các Tab chuyển đổi mượt mà với hiệu ứng thẻ nổi và bóng đổ 3D.
- **Chế độ Sáng ☀️ / Tối 🌙 (Light / Dark Mode Switcher)**: Chuyển đổi linh hoạt giao diện ban ngày và ban đêm ngay trên Sidebar.
- **Sidebar Glassmorphism**: Thanh bên cố định hiện đại với hiệu ứng kính mờ và nút đóng/mở hình tròn.
- **Thanh cuộn siêu mỏng (Global Webkit & Firefox Scrollbar)**: Loại bỏ thanh cuộn thô kệch, tạo cảm giác mượt mà (butter-smooth).

---

## 🏗️ Động Cơ AI & Xử Lý Ngôn Ngữ Tự Nhiên

- **Google Gemini 3.5 Flash Model**: Tốc độ xử lý siêu nhanh với chi phí tối ưu.
- **Structured Outputs Schema**: Sử dụng `Pydantic` / `TypedDict` đảm bảo kết quả trả về từ AI luôn tuân thủ 100% định dạng JSON hợp lệ:
  ```json
  {
    "type": "Chi",
    "amount": 35000,
    "category": "Ăn uống & Cafe",
    "description": "Ăn phở sáng"
  }
  ```

---

## 🚀 Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Yêu Cầu Tiên Quyết
- **Python 3.10+** (Khuyên dùng Python 3.12).
- **Git** đã được cài đặt.

### 2. Tải Mã Nguồn & Cài Đặt Thư Viện
```bash
# Clone kho lưu trữ
git clone https://github.com/proyctk03-eng/quan-ly-thu-chi-ai.git
cd quan-ly-thu-chi-ai

# Cài đặt các thư viện phụ thuộc
pip install -r 02_MaNguon_ChuongTrinh/requirements.txt
```

### 3. Cấu Hình Biến Môi Trường (.env)
```bash
# Tạo file .env từ file mẫu
cp 02_MaNguon_ChuongTrinh/.env.example .env

# Mở file .env và điền API Key Google Gemini của bạn
GEMINI_API_KEY=AIzaSy...YourActualGeminiApiKey
```
> 💡 *Bạn có thể nhận Gemini API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/).*

### 4. Khởi Chạy Ứng Dụng Web
```bash
streamlit run 02_MaNguon_ChuongTrinh/app.py
```
👉 Trình duyệt sẽ tự động mở địa chỉ: `http://localhost:8501`

---

## 🐳 Triển Khai Với Docker

Ứng dụng được đóng gói sẵn Docker để triển khai dễ dàng trên bất kỳ máy chủ nào:

```bash
cd 02_MaNguon_ChuongTrinh

# Khởi chạy ứng dụng với Docker Compose
docker-compose up --build -d
```
Ứng dụng sẽ hoạt động tại địa chỉ: `http://localhost:8501`

---

## 🧪 Kiểm Thử Tự Động (Automated Testing)

Dự án được trang bị bộ kiểm thử tự động **Pytest** bao phủ 100% các chức năng cốt lõi:

```bash
# Chạy bộ test suite
pytest 02_MaNguon_ChuongTrinh/test_main.py -v
```

**Kết quả kiểm thử:**
- `test_create_tables`: PASSED (Khởi tạo CSDL SQLite thành công).
- `test_insert_transaction`: PASSED (Thêm giao dịch chuẩn xác).
- `test_delete_transaction`: PASSED (Xóa giao dịch an toàn).
- `test_update_transaction`: PASSED (Cập nhật giao dịch).
- `test_budget_limit`: PASSED (Đặt hạn mức ngân sách).
- `test_financial_summary`: PASSED (Tính toán tổng thu, chi, số dư).
- `test_category_mapping`: PASSED (Ánh xạ danh mục sinh viên).
- `test_money_slang_conversion`: PASSED (Quy đổi slang 'k', 'củ', 'm').
- `test_env_file_exists`: PASSED (Xác minh môi trường bảo mật).
- `test_student_categories`: PASSED (Danh mục sinh viên hợp lệ).

👉 **Tỷ lệ vượt qua: 10/10 PASS (100%)**

---

## 📂 Cấu Trúc Dự Án

```
quan-ly-thu-chi-ai/
├── 📁 01_BaoCao_TàiLieu_Va_SoDo/      # Báo cáo đồ án (.docx, .md) & sơ đồ quy trình
│   ├── 01_project-plan.md              # Kế hoạch phát triển dự án
│   ├── 02_requirements-qa.md           # Yêu cầu hệ thống & Q&A
│   ├── 03_requirements-specification.md # Đặc tả yêu cầu phần mềm (SRS)
│   ├── 04_object-oriented-design.md    # Thiết kế hướng đối tượng (OOD)
│   ├── 05_functional-testing.md        # Kịch bản kiểm thử chức năng
│   ├── 06_database.md                  # Thiết kế cơ sở dữ liệu SQLite
│   ├── 07_user-guide.md                # Hướng dẫn sử dụng cho sinh viên
│   ├── BAO_CAO_AP_DUNG_PROMPT_AI.md     # Báo cáo kỹ thuật Prompt Engineering
│   └── system_architecture_diagram.html # Sơ đồ kiến trúc hệ thống
│
├── 📁 02_MaNguon_ChuongTrinh/          # Gói mã nguồn chương trình chính
│   ├── 📁 backend/                     # REST API FastAPI backend (mở rộng microservices)
│   ├── 📁 frontend/                    # Giao diện frontend Streamlit
│   ├── 📁 tests/                       # Thư mục chứa các bài unit test
│   ├── app.py                          # Mã nguồn ứng dụng Web chính
│   ├── test_main.py                    # Script chạy kiểm thử Pytest
│   ├── requirements.txt                # Danh sách thư viện Python
│   ├── Dockerfile                      # File đóng gói Docker container
│   ├── docker-compose.yml              # File cấu hình Docker Compose
│   └── .env.example                    # File mẫu biến môi trường
│
├── .gitignore                          # Danh sách loại trừ Git
├── app.py                              # Trỏ tới mã nguồn ứng dụng chính
└── README.md                           # Tài liệu tài nguyên dự án (file này)
```

---

## 👥 Nhóm Thực Hiện

- **Dự án**: Đồ Án Phát Triển Phần Mềm Hướng Tác Thể & GenAI
- **Nhóm**: Nhóm 02
- **Tên dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI
- **Repository**: [proyctk03-eng/quan-ly-thu-chi-ai](https://github.com/proyctk03-eng/quan-ly-thu-chi-ai)

---

<div align="center">
  <sub>Made with ❤️ for Students | Powered by <strong>Google Gemini AI</strong> & <strong>Streamlit</strong></sub>
</div>
