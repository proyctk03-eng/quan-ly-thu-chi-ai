# 03 - ĐẶC TẢ YÊU CẦU PHẦN MỀM (SOFTWARE REQUIREMENTS SPECIFICATION - SRS)

## 1. Giới thiệu
Tài liệu đặc tả yêu cầu phần mềm theo chuẩn IEEE 830 cho ứng dụng Quản lý Chi tiêu Sinh viên AI.

## 2. Yêu cầu chức năng chi tiết (Functional Requirements)
- **FR-01**: Khởi tạo CSDL SQLite chi_tieu.db tự động với các bảng giao_dich và han_muc.
- **FR-02**: Bóc tách thu chi tự nhiên bằng Gemini AI Flash (analyze_natural_language_expense).
- **FR-03**: Trợ lý CSKH Agentic FAB button fixed góc phải viewport (chat_with_gemini_agent).
- **FR-04**: Biểu đồ phân tích Plotly (Pie chart, Bar chart, Line chart tích lũy).
- **FR-05**: Xuất dữ liệu CSV/Excel và Nhập file CSV tự động.

## 3. Yêu cầu phi chức năng (Non-Functional Requirements)
- **NFR-01 (Hiệu năng)**: Xử lý giao dịch SQLite < 0.1s, Phản hồi Gemini API < 2s.
- **NFR-02 (Bảo mật)**: Tải API Key bảo mật qua load_dotenv và st.secrets.
