# 05 - KỊCH BẢN VÀ KẾT QUẢ KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TESTING)

## 1. Kế hoạch kiểm thử (Test Plan)
Sử dụng framework pytest để kiểm thử tự động toàn bộ Data Engine và Logic Chuyển Đổi.

## 2. Danh sách Test Cases (test_main.py)
1. test_create_tables: Kiểm tra khởi tạo bảng giao_dich và han_muc. [PASSED]
2. test_insert_transaction: Kiểm tra thêm giao dịch thành công. [PASSED]
3. test_delete_transaction: Kiểm tra xóa giao dịch theo ID. [PASSED]
4. test_update_transaction: Kiểm tra cập nhật giao dịch. [PASSED]
5. test_budget_limit: Kiểm tra đặt và truy vấn hạn mức. [PASSED]
6. test_financial_summary: Kiểm tra tính toán Tổng Thu, Tổng Chi, Số Dư. [PASSED]
7. test_category_mapping: Kiểm tra chuẩn hóa danh mục sinh viên. [PASSED]
8. test_money_slang_conversion: Kiểm tra quy đổi số tiền từ lóng (k, củ). [PASSED]
9. test_env_file_exists: Kiểm tra sự tồn tại của file cấu hình .env. [PASSED]
10. test_student_categories: Kiểm tra danh sách 9 danh mục sinh viên chuẩn. [PASSED]

👉 Kết quả: 10/10 Test Cases PASSED (100%).
