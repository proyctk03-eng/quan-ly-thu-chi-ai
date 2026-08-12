# THU THẬP VÀ LÀM RÕ YÊU CẦU DỰ ÁN (REQUIREMENTS QA)

**Dự án**: Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓  
**Nhóm**: Nhóm 01 - CNTT K23K  

---

## Bảng Danh Sách Câu Hỏi Làm Rõ Yêu Cầu (QA-001 đến QA-020)

| STT | Câu hỏi (Questions) | Trả lời (Answers) | Ghi chú & Trạng thái |
|-----|----------------------|-------------------|----------------------|
| 1 | Người dùng mục tiêu của hệ thống là ai? | Sinh viên đại học/cao đẳng cần theo dõi ví cá nhân và nhận tư vấn tài chính. | Đã trả lời |
| 2 | Đơn vị tiền tệ chính và cách xử lý từ lóng tiền tệ? | Tiền tệ VNĐ. AI tự động quy đổi `k` (1.000), `lít/loét` (100.000), `củ/triệu` (1.000.000). | Đã trả lời |
| 3 | Các danh mục chi tiêu dành riêng cho sinh viên? | 9 danh mục: Ăn uống & Cafe, Tiền nhà & Tiện ích, Học tập & Sách vở, Di chuyển & Xăng xe, Giải trí & Bè bạn, Mua sắm cá nhân, Chu cấp gia đình, Đi làm thêm, Khác. | Đã trả lời |
| 4 | Mô hình kiến trúc ứng dụng được lựa chọn? | Decoupled Architecture: Backend FastAPI REST API (port 8000), Frontend Streamlit UI (port 8502). | Đã trả lời |
| 5 | Các tính năng AI chính trong hệ thống? | (1) AI Bóc tách chi tiêu từ tiếng Việt tự nhiên; (2) AI Tư vấn tiết kiệm & toán học; (3) AI Chatbot; (4) AI CSKH Agentic. | Đã trả lời |
| 6 | Cơ chế xử lý lỗi Geo-blocking khi gọi Gemini API? | Tự động đọc `HTTP_PROXY`/`HTTPS_PROXY` từ `.env`, gán vào `os.environ` và bắt lỗi trả về `GEO_BLOCK_MSG`. | Đã trả lời |
| 7 | Phương thức sao lưu và xuất dữ liệu? | Hỗ trợ xuất file báo cáo CSV (`utf-8-sig`) và Excel (`.xlsx`), hỗ trợ nhập file CSV. | Đã trả lời |
| 8 | Phương thức xác nhận khi xóa giao dịch? | Xác nhận 2 bước: chọn ID giao dịch, hiển thị box cảnh báo và checkbox xác nhận trước khi nút Xóa hoạt động. | Đã trả lời |
| 9 | Cách đóng gói ứng dụng để triển khai? | Sử dụng Dockerfile multi-stage và `docker-compose.yml` chạy 2 container backend & frontend. | Đã trả lời |
| 10 | Các chỉ số thống kê tài chính hiển thị trên giao diện? | Tổng thu, tổng chi, số dư ví, tỷ lệ tiết kiệm %, chỉ số sức khỏe tài chính, so sánh tháng này vs tháng trước. | Đã trả lời |
