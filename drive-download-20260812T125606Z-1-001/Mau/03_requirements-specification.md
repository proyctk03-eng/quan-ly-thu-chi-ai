# ĐẶC TẢ YÊU CẦU PHẦN MỀM (SOFTWARE REQUIREMENTS SPECIFICATION - SRS)

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 01 - CNTT K23K  

---

## 1. Giới Thiệu & Phạm Vi Hệ Thống

Tài liệu SRS đặc tả chính thức các yêu cầu chức năng, yêu cầu phi chức năng và giao diện cho ứng dụng **Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓**.

## 2. Danh Sách Use Cases Chính

- **UC001_Quản lý giao dịch thu chi**: Thêm thủ công, chỉnh sửa, xóa có xác nhận 2 bước, danh sách bộ lọc theo từ khóa, danh mục, tháng.
- **UC002_Quản lý hạn mức ngân sách**: Đặt hạn mức chi tiêu theo 6 danh mục chính, hiển thị progress bar cảnh báo vượt hạn mức.
- **UC003_Thống kê & Phân tích tài chính**: Hiển thị metric cards (Tổng thu, Tổng chi, Số dư ví), so sánh tháng này vs tháng trước, tỷ lệ tiết kiệm %, biểu đồ Plotly (Pie, Bar, Line trend).
- **UC004_Xuất nhập dữ liệu CSV/Excel**: Export dữ liệu ra CSV utf-8-sig / Excel .xlsx, import file CSV dồn dữ liệu.
- **UC005_AI Bóc tách giao dịch tự nhiên**: Trích xuất loại, số tiền, danh mục, warning level (SAFE/WARNING/CRITICAL), gợi ý sinh viên từ câu nhập.
- **UC006_AI Tư vấn tiết kiệm & Hỗ trợ học tập**: Phân tích lịch sử chi tiêu CSV và tư vấn tiết kiệm, hỗ trợ giải bài tập toán học.
- **UC007_AI Chatbot & CSKH Agentic**: Khung chat nổi popover thực thi lệnh hệ thống (Thêm/Xóa/Đặt hạn mức) qua ngôn ngữ tự nhiên.
- **UC008_Cấu hình Proxy & Vượt Geo-blocking**: Đọc HTTP_PROXY từ `.env`, tự động inject vào `os.environ` và hiển thị hướng dẫn khi bị chặn địa lý.

## 3. Yêu Cầu Chức Năng (Functional Requirements)
- **FR001**: Hệ thống phải cung cấp RESTful API đầy đủ CRUD tại `/api/transactions`, `/api/budgets`, `/api/analytics`, `/api/ai`.
- **FR002**: Hệ thống phải tự động tính toán tổng thu, tổng chi và số dư thời gian thực.
- **FR003**: Hệ thống phải hỗ trợ lọc danh sách giao dịch theo 3 tiêu chí độc lập hoặc kết hợp: Từ khóa ghi chú, Danh mục, Tháng.

## 4. Yêu Cầu Phi Chức Năng (Non-Functional Requirements)
- **NFR001 (Performance)**: Phản hồi REST API < 500ms cho các thao tác CSDL SQLite và < 3s cho các lệnh gọi Gemini AI.
- **NFR002 (Security)**: Giữ an toàn GEMINI_API_KEY trong file `.env`, không lộ key trên giao diện Client.
- **NFR003 (Usability)**: Giao diện Streamlit responsive, hỗ trợ đổi Light/Dark theme theo cài đặt trình duyệt.
- **NFR004 (Portability)**: Đóng gói thành công trong Docker container.
