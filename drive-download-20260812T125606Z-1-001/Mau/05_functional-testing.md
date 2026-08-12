# BÁO CÁO KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TESTING)

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 01 - CNTT K23K  

---

## 1. Môi Trường & Tài Nguyên Kiểm Thử
- **Phần cứng**: CPU Intel/AMD, RAM 8GB, kết nối Internet / Proxy.
- **Môi trường phần mềm**: Python 3.12, Pytest 9.1, FastAPI TestClient, Request library.

## 2. Kịch Bản & Kết Quả Kiểm Thử API Integration (tests/test_api.py)

| Test ID | Tên Kịch Bản Kiểm Thử | Endpoint / Function | Trạng thái | Thời gian |
|---------|-----------------------|---------------------|------------|-----------|
| TC01 | Kiểm tra Health Check Backend | `GET /health` | **PASSED** | 0.05s |
| TC02 | Lấy danh sách giao dịch | `GET /api/transactions` | **PASSED** | 0.12s |
| TC03 | Thêm mới & Xóa giao dịch | `POST /api/transactions` -> `DELETE` | **PASSED** | 0.25s |
| TC04 | Lấy danh sách hạn mức | `GET /api/budgets` | **PASSED** | 0.08s |
| TC05 | Đặt hạn mức chi tiêu | `POST /api/budgets` | **PASSED** | 0.15s |
| TC06 | Thống kê tổng thu/chi/số dư | `GET /api/analytics/summary` | **PASSED** | 0.10s |
| TC07 | So sánh chi tiêu tháng | `GET /api/analytics/monthly-comparison` | **PASSED** | 0.14s |
| TC08 | Quy đổi từ lóng VNĐ (199k, 5 củ) | `test_money_slang_conversion` | **PASSED** | 0.04s |
| TC09 | Kiểm tra file môi trường .env | `test_env_file_exists` | **PASSED** | 0.01s |
| TC10 | Geo-blocking proxy fallback | `test_is_geo_blocked_error` | **PASSED** | 0.02s |

**Tổng kết**: **100% PASSED** (10/10 unit tests & 7/7 REST API integration tests).
