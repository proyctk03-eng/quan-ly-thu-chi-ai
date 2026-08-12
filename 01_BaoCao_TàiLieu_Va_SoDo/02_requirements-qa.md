# 02 - PHỎNG VẤN VÀ LÀM SÁNG TỎ YÊU CẦU (REQUIREMENTS Q&A)

## 1. Các câu hỏi nghiệp vụ làm rõ
- **Q1**: Làm thế nào để AI nhận diện các từ lóng số tiền sinh viên thường dùng?
  - **A1**: Sử dụng quy tắc Prompt Constraints: 199k -> 199.000 VNĐ, 5 củ -> 5.000.000 VNĐ, lít/loét -> 100.000 VNĐ. Nếu có nhiều khoản chi trong 1 câu, cộng tổng lại.
- **Q2**: Tiêu chí đánh giá mức độ rủi ro chi tiêu là gì?
  - **A2**: SAFE (chi hợp lý), WARNING (gần chạm hạn mức), CRITICAL (vượt quá số dư ví / sụt giảm nghiêm trọng tài chính).
- **Q3**: Phạm vi trả lời của Trợ lý AI Gemini được kiểm soát như thế nào?
  - **A3**: Áp dụng quy tắc Allowlist (Tài chính & Toán học) và Denylist (Từ chối 100% câu hỏi ngoài phạm vi bằng mẫu câu chuẩn).
