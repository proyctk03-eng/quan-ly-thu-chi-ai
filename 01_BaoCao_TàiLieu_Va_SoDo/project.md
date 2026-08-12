# ĐỀ TÀI: HỆ THỐNG QUẢN LÝ CHI TIÊU SINH VIÊN TÍCH HỢP AI GEMINI

## 1. Mô tả bài toán
Sinh viên đại học thường gặp khó khăn lớn trong quản lý thu chi:
- Tiêu xài không kiểm soát dẫn đến nguy cơ cháy túi giữa tháng, bẫy nợ nần, thiếu tiền nhà và học phí.
- Công cụ quản lý truyền thống rườm rà, tốn thời gian nhập liệu thủ công.
- Rào cản tâm lý khi không có cố vấn đưa ra lời khuyên tài chính sát với thực tế sinh viên.

Giải pháp **Sổ Tay Sinh Viên 🎓** cung cấp:
- Nhập thu chi tự nhiên: AI bóc tách tiền từ lóng ('199k', '5 củ', '30k trưa'), tự cộng dồn nhiều khoản.
- Cảnh báo rủi ro & hệ lụy: Đánh giá SAFE / WARNING / CRITICAL dựa trên số dư ví & hạn mức.
- Trợ lý CSKH Agentic (FAB popover nổi góc phải viewport): Thực thi CRUD tự động (Thêm/Xóa/Hạn mức).
- Trực quan hóa dữ liệu bằng Plotly linh hoạt, bộ test case pytest tự động đạt 100% pass.

## 2. Mục tiêu hệ thống
- Tự động hóa quản lý ví cá nhân với cơ sở dữ liệu SQLite tốc độ cao.
- Tích hợp Google Gemini Flash API theo chuẩn cấu trúc Prompt Engineering 5 phần.
- Chặn tuyệt đối câu hỏi ngoài phạm vi (Allowlist tài chính & toán học, Denylist chủ đề phiếm).
- Thiết kế giao diện Streamlit hiện đại, tương thích Light/Dark Mode.

## 3. Yêu cầu chức năng
1. Thống kê số dư, tổng thu, tổng chi, tỷ lệ tiết kiệm & cảnh báo hết tiền.
2. Thêm khoản thu chi thủ công hoặc chat bóc tách tự nhiên.
3. Lịch sử giao dịch, tìm kiếm, lọc theo tháng/danh mục, sửa/xóa với checkbox xác nhận.
4. Gợi ý tiết kiệm tự động từ dữ liệu CSV.
5. Trợ lý hỏi đáp tài chính & giải bài tập toán học.
6. CSKH Floating Action Button (FAB popover fixed bottom-right).

## 4. Yêu cầu phi chức năng
- Thời gian phản hồi < 2s.
- Bảo mật API Key qua .env và st.secrets.
- Đạt 10/10 test unit cases với pytest.
