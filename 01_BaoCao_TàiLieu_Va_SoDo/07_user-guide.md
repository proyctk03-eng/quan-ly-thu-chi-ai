# 07 - HƯỚNG DẪN SỬ DỤNG SỔ TAY QUẢN LÝ CHI TIÊU SINH VIÊN AI 🎓

## 1. Hướng dẫn Cài đặt & Khởi chạy
1. Cài đặt các thư viện phụ thuộc:
   pip install streamlit pandas plotly google-generativeai python-dotenv pytest openpyxl
2. Cấu hình Gemini API Key vào file .env:
   GEMINI_API_KEY=AIzaSy...
3. Chạy ứng dụng Streamlit:
   streamlit run app.py

## 2. Hướng dẫn Sử dụng Các Tính Năng
- Nhập chi tiêu nhanh qua AI: Vào Tab 2, gõ câu ví dụ: 'Trưa ăn phở 35k cafe 25k', nhấn Enter. AI sẽ tự bóc tách tổng tiền 60.000 ₫, hiển thị mức độ rủi ro SAFE và bấm Xác nhận để lưu.
- Điều hành qua Trợ lý CSKH (Nút Tròn FAB): Nhấn vào icon 💬 ở góc dưới bên phải màn hình. Gõ: 'Thêm chi xăng xe 50k' hoặc 'Xóa giao dịch 3', AI CSKH sẽ tự động thực thi.
- Xuất file báo cáo: Vào Tab 3, chọn Tải Báo Cáo CSV hoặc Tải Báo Cáo Excel (.xlsx).
