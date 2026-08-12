# 04 - THIẾT KẾ HƯỚNG ĐỐI TƯỢNG VÀ KIẾN TRÚC (OBJECT-ORIENTED DESIGN - OOD)

## 1. Kiến trúc hệ thống
Hệ thống thiết kế theo kiến trúc Layered Architecture kết hợp Component-Based UI trong Streamlit:
- **Presentation Layer**: Streamlit Tabs, Sidebar, Floating Popover CSKH Widget, Plotly Charts.
- **Service / AI Layer**: init_gemini(), analyze_natural_language_expense(), generate_savings_advice(), chat_with_gemini(), chat_with_gemini_agent().
- **Data Access Layer**: get_db_connection(), init_db(), add_transaction(), update_transaction(), delete_transaction(), set_budget_limit().
- **Database**: SQLite Engine (chi_tieu.db).

## 2. Sơ đồ Kiến trúc & Luồng xử lý Hệ thống (System Architecture Diagram)
Sơ đồ kiến trúc hệ thống và luồng dữ liệu giữa Streamlit UI Frontend, FastAPI Backend Router, Google Gemini Flash API và CSDL SQLite đã được xuất ra file đồ họa vector tương tác:
👉 **[system_architecture_diagram.html](system_architecture_diagram.html)**

### Chi tiết các tầng kiến trúc:
- **Presentation Layer (Frontend)**: Streamlit Dashboard UI & Mini CSKH FAB Widget.
- **Application & AI Services (Backend API)**: FastAPI Backend Router (Port 8000), Gemini Flash LLM Service.
- **Data Persistence & Audit**: SQLite Storage (`chi_tieu.db`) & Pytest Automation Audit Suite.

## 3. Thiết kế Lớp (Class & Schema)
- TransactionSchema(TypedDict): Schema định dạng JSON trả về từ Gemini API (type, amount, category, description).
- giao_dich: Entity đại diện cho bảng CSDL giao dịch.
- han_muc: Entity đại diện cho ngân sách hạn mức danh mục.
