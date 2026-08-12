# KẾ HOẠCH THỰC HIỆN DỰ ÁN SDLC

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 02 - CNTT K23K  
**Thành viên**: Nguyễn Tuấn Đạt (Trưởng nhóm), Phàn Ngọc Anh (Phó nhóm)  
**Thời gian**: 27/07/2026 - 27/09/2026 (9 tuần)  

## 1. Mục Tiêu Dự Án (OBJ-001)
- **OBJ-001**: Xây dựng ứng dụng sổ tay chi tiêu cá nhân dành cho sinh viên với 9 danh mục thực tế.
- **OBJ-002**: Kiến trúc Decoupled: Backend RESTful API bằng FastAPI, Frontend UI bằng Streamlit.
- **OBJ-003**: Tích hợp Google Gemini AI Engine bóc tách thu chi tiếng Việt tự nhiên ("Sáng ăn phở 35k"), quy đổi từ lóng (k, củ, lít), gợi ý tiết kiệm và CSKH Agentic.
- **OBJ-004**: Hỗ trợ cơ chế Proxy tự động và nạp thông báo vượt Geo-blocking an toàn.
- **OBJ-005**: Container hóa giải pháp với Docker & Docker Compose.

## 2. Kế Hoạch 9 Tuần
- **Tuần 1**: Lập kế hoạch dự án (Project Plan), khảo sát nhu cầu quản lý ví sinh viên.
- **Tuần 2**: Thu thập và làm rõ yêu cầu phần mềm (Requirements QA), 20 câu hỏi QA.
- **Tuần 3**: Xây dựng đặc tả yêu cầu phần mềm (SRS), Use Cases (UC001-UC008), FR và NFR.
- **Tuần 4**: Thiết kế hướng đối tượng (OOD), Pydantic Schemas, Layered Architecture.
- **Tuần 5**: Thiết kế Cơ sở dữ liệu SQLite (`giao_dich`, `han_muc`) & Sơ đồ luồng màn hình.
- **Tuần 6**: Lập trình Backend FastAPI REST API (`backend/`) & CRUD nghiệp vụ.
- **Tuần 7**: Tích hợp Gemini AI Engine (`ai_service.py`), bóc tách chi tiêu, CSKH Agentic.
- **Tuần 8**: Kiểm thử chức năng Functional Testing (Pytest 100% PASS) & Docker containerization.
- **Tuần 9**: Hoàn thiện tài liệu User Guide, tổng kết dự án, review code & nghiệm thu.
