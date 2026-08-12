# TÀI LIỆU THIẾT KẾ HƯỚNG ĐỐI TƯỢNG (OOD)

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 01 - CNTT K23K  

---

## 1. Kiến Trúc Phân Lớp Hệ Thống (Decoupled Layered Architecture)

Hệ thống được thiết kế theo mô hình 4 lớp rõ ràng:

1. **Presentation Layer (Frontend)**: `frontend/app.py` xây dựng bằng Streamlit UI, gọi Backend qua `requests`.
2. **API Controller Layer (FastAPI Routers)**: `backend/api/routes/` gồm `transactions.py`, `budgets.py`, `analytics.py`, `ai.py`.
3. **Business Service Layer**: `backend/services/` gồm `transaction_service.py`, `budget_service.py`, `analytics_service.py`, `ai_service.py`.
4. **Core & Data Access Layer**: `backend/core/` (`config.py`, `database.py`) kết nối SQLite `chi_tieu.db` và nạp cấu hình Proxy.

## 2. Chi Tiết Các Class & Schemas Pydantic

- **TransactionCreate / TransactionUpdate / TransactionResponse**: Pydantic models quản lý dữ liệu giao dịch.
- **BudgetLimitSet / BudgetLimitResponse**: Pydantic models quản lý hạn mức.
- **SummaryResponse / MonthlyComparisonResponse**: Schemas dữ liệu thống kê tài chính.
- **AIParseRequest / AIChatRequest / AIAgentRequest / AIResponse**: Schemas trao đổi dữ liệu AI API.
- **TransactionService**: Hàm static `list_transactions()`, `add_transaction()`, `update_transaction()`, `delete_transaction()`.
- **AIService**: Hàm static `init_gemini()`, `analyze_natural_language_expense()`, `generate_savings_advice()`, `chat_with_gemini()`, `chat_with_gemini_agent()`.
