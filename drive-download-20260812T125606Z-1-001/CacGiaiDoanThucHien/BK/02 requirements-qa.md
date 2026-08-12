# Prompt

Bạn là **Business Analyst (BA)**, **Product Owner (PO)**, **System Analyst** và **Technical Writer** có kinh nghiệm thực hiện **Requirements Elicitation** và **Requirements Analysis** trong dự án phần mềm có tích hợp **Generative AI**.

Bạn có chuyên môn về:

* BABOK v3;
* Requirements Engineering;
* Stakeholder Analysis;
* Interview and Survey Design;
* Business Process Analysis;
* User Story Mapping;
* Agile/Scrum;
* Prompt Engineering;
* AI-Augmented SDLC.

Nhiệm vụ của bạn là xây dựng tài liệu **Requirements QA** để thu thập, phân tích, làm rõ và chuẩn bị yêu cầu trước khi chuyển sang tài liệu đặc tả yêu cầu chính thức.

---

# Mục tiêu

Hoàn thiện tài liệu:

```text
02_GenAI_SoftwareDevelopment_requirements-qa.docx
```

Tài liệu này tập trung vào:

* xác định stakeholder;
* thu thập câu hỏi làm rõ yêu cầu;
* ghi nhận câu trả lời nếu có;
* phát hiện thiếu sót, mơ hồ và mâu thuẫn;
* xác định giả định;
* xác định Open Questions;
* ghi nhận quyết định sau khi làm rõ;
* chuẩn bị đầu vào cho tài liệu SRS.

Không viết lại đầy đủ yêu cầu dưới dạng đặc tả chính thức. Các yêu cầu được chuẩn hóa sẽ thuộc tài liệu:

```text
03_GenAI_SoftwareDevelopment_requirements-specification.docx
```

---

# Nguồn dữ liệu đầu vào

Trước khi viết tài liệu, hãy đọc đầy đủ:

```text
informember.md
project.md
01_GenAI_SoftwareDevelopment_project-plan.docx
```

Trong đó:

* `informember.md` chứa thông tin nhóm, thành viên và vai trò;
* `project.md` chứa mô tả bài toán, mục tiêu, phạm vi, chức năng và công nghệ dự kiến;
* `01_GenAI_SoftwareDevelopment_project-plan.docx` chứa kế hoạch thực hiện, sprint, deliverable và định hướng sử dụng AI.

Nếu file Word kế hoạch chưa có hoặc chưa đủ thông tin, tiếp tục dựa trên `informember.md` và `project.md`, đồng thời ghi rõ giả định.

---

# Phạm vi của tài liệu Requirements QA

Tài liệu này được dùng để ghi nhận quá trình làm rõ yêu cầu, không phải tài liệu đặc tả chính thức.

Nội dung được phép trình bày chi tiết:

* stakeholder;
* mục tiêu thu thập yêu cầu;
* câu hỏi BA cần hỏi;
* câu trả lời hoặc trạng thái chưa có câu trả lời;
* vấn đề cần làm rõ;
* giả định;
* mâu thuẫn;
* quyết định làm rõ;
* yêu cầu dự kiến sẽ chuyển sang SRS;
* rủi ro yêu cầu.

Không trình bày chi tiết:

* toàn bộ Functional Requirement theo cấu trúc SRS;
* toàn bộ Non-functional Requirement theo tiêu chí nghiệm thu;
* class, method, sequence diagram;
* test case chi tiết.

---

# Quy ước mã định danh

Sử dụng mã thống nhất:

| Loại nội dung | Mã |
| --- | --- |
| Câu hỏi làm rõ | `QA-001` |
| Giả định | `ASM-001` |
| Câu hỏi mở | `OQ-001` |
| Quyết định làm rõ | `DEC-001` |
| Yêu cầu dự kiến | `FR-DRAFT-001`, `NFR-DRAFT-001`, `AIR-DRAFT-001` |
| Rủi ro yêu cầu | `RR-001` |

Các mã dự kiến chỉ dùng trong tài liệu QA. Khi sang SRS, yêu cầu phải được chuẩn hóa thành mã chính thức như `FR-001`, `NFR-001`, `AIR-001`.

---

# Quy trình thực hiện

## Bước 1. Đọc và tổng hợp dữ liệu

Tổng hợp:

* tên dự án;
* mục tiêu hệ thống;
* bối cảnh nghiệp vụ;
* phạm vi tổng quan;
* stakeholder;
* module/chức năng được nhắc đến;
* chức năng AI được nhắc đến;
* dữ liệu chính;
* ràng buộc;
* sprint hoặc milestone liên quan;
* điểm chưa rõ.

## Bước 2. Phân tích stakeholder

Xác định các bên liên quan:

* Customer/End User;
* Product Owner;
* Instructor;
* Project Manager;
* Developer;
* Tester;
* Admin;
* Nhân viên bán hàng;
* Quản lý;
* AI Assistant;
* hệ thống hoặc dịch vụ bên ngoài nếu có.

Mỗi stakeholder cần có:

* mã stakeholder;
* tên;
* vai trò;
* mục tiêu;
* thông tin cần khai thác;
* mức ảnh hưởng;
* trạng thái xác nhận.

## Bước 3. Thiết kế câu hỏi làm rõ

Sinh khoảng **50 đến 80 câu hỏi** theo nhóm:

* nghiệp vụ;
* người dùng;
* quy trình bán hàng;
* sản phẩm và danh mục;
* khách hàng;
* đơn hàng và hóa đơn;
* báo cáo;
* dữ liệu;
* phân quyền;
* AI;
* bảo mật;
* hiệu năng;
* triển khai;
* chi phí;
* mở rộng.

Mỗi câu hỏi cần có:

* mã `QA-xxx`;
* nhóm câu hỏi;
* nội dung câu hỏi;
* mục đích hỏi;
* stakeholder cần trả lời;
* câu trả lời nếu đã có;
* trạng thái: `Đã rõ`, `Cần xác nhận`, `Chưa có thông tin`;
* yêu cầu dự kiến liên quan.

## Bước 4. Phân tích điểm mơ hồ và mâu thuẫn

Tạo bảng ghi nhận:

| ID | Nội dung | Vấn đề | Ảnh hưởng | Đề xuất làm rõ | Trạng thái |
| --- | --- | --- | --- | --- | --- |

Ví dụ, nếu có yêu cầu "tìm kiếm nhanh", cần làm rõ:

* nhanh là bao nhiêu giây;
* tìm theo tên, mã, barcode hay từ khóa;
* có cần fuzzy search, full-text search hoặc AI search không;
* phạm vi dữ liệu tìm kiếm;
* người dùng nào được sử dụng.

## Bước 5. Ghi nhận Assumptions và Open Questions

Tạo danh sách:

* `ASM-xxx`: giả định hợp lý để tiếp tục phân tích;
* `OQ-xxx`: câu hỏi chưa thể kết luận và cần xác nhận.

Mỗi mục cần có:

* mô tả;
* lý do;
* ảnh hưởng;
* người cần xác nhận;
* tài liệu hoặc yêu cầu liên quan.

## Bước 6. Xác định yêu cầu dự kiến chuyển sang SRS

Tạo bảng ánh xạ:

| QA ID | Nội dung đã làm rõ | Yêu cầu dự kiến | Loại yêu cầu | Ghi chú cho SRS |
| --- | --- | --- | --- | --- |

Không đặc tả đầy đủ ở bước này. Chỉ xác định yêu cầu sẽ được chuẩn hóa trong tài liệu SRS.

## Bước 7. Hoàn thiện tài liệu Word

Ghi nội dung vào:

```text
02_GenAI_SoftwareDevelopment_requirements-qa.docx
```

Giữ nguyên cấu trúc, Heading, style, bảng biểu và định dạng của template.

---

# Cấu trúc nội dung cần hoàn thiện

## 1. Giới thiệu

Bao gồm:

* mục đích tài liệu;
* phạm vi tài liệu;
* đối tượng sử dụng;
* phương pháp thu thập yêu cầu;
* tài liệu tham khảo.

## 2. Tổng quan dự án ở góc nhìn yêu cầu

Tóm tắt ngắn gọn:

* bối cảnh;
* mục tiêu;
* phạm vi;
* module chính;
* chức năng AI;
* các điểm cần làm rõ.

Không lặp lại toàn bộ Project Plan.

## 3. Stakeholder Analysis

Lập bảng stakeholder với mục tiêu, thông tin cần khai thác và mức ảnh hưởng.

## 4. Requirements Elicitation Questions

Lập danh sách câu hỏi theo nhóm, có mã `QA-xxx` và trạng thái rõ ràng.

## 5. Clarification Log

Ghi nhận nội dung đã được làm rõ, quyết định liên quan và yêu cầu dự kiến.

## 6. Ambiguity and Conflict Analysis

Ghi nhận các điểm mơ hồ, thiếu hoặc mâu thuẫn.

## 7. Assumptions

Liệt kê giả định theo mã `ASM-xxx`.

## 8. Open Questions

Liệt kê câu hỏi mở theo mã `OQ-xxx`.

## 9. Draft Requirement Mapping

Ánh xạ câu hỏi/điểm làm rõ sang yêu cầu dự kiến trong SRS.

## 10. AI Support in Requirements QA

Mô tả cách AI hỗ trợ:

* gợi ý câu hỏi;
* phát hiện điểm mơ hồ;
* nhóm yêu cầu;
* chuẩn hóa thuật ngữ;
* đề xuất assumption;
* kiểm tra tính nhất quán.

Đồng thời nêu rõ: mọi kết quả AI phải được con người kiểm chứng.

## 11. Kết luận

Tóm tắt:

* các nhóm yêu cầu đã làm rõ;
* các vấn đề còn mở;
* các giả định quan trọng;
* đầu vào cần chuyển sang SRS.

---

# Quy tắc chỉnh sửa tài liệu Word

Giữ nguyên:

* Heading;
* style;
* font;
* bảng;
* đánh số;
* bố cục;
* định dạng.

Chỉ điền hoặc thay thế nội dung trong các vị trí phù hợp.

---

# Yêu cầu chất lượng

Tài liệu phải:

* tập trung đúng vào hoạt động thu thập và làm rõ yêu cầu;
* không lặp lại chi tiết SRS;
* câu hỏi cụ thể, có mục đích rõ ràng;
* mỗi giả định hoặc câu hỏi mở có mã định danh;
* có trạng thái xử lý rõ ràng;
* có ánh xạ sang yêu cầu dự kiến;
* phù hợp với phạm vi nhóm sinh viên;
* sử dụng thuật ngữ nhất quán với Project Plan.

---

# Đầu ra mong muốn

Lưu tài liệu hoàn chỉnh vào:

```text
02_GenAI_SoftwareDevelopment_requirements-qa.docx
```

Sau khi hoàn thành, báo cáo ngắn gọn:

* số lượng stakeholder;
* số lượng câu hỏi QA;
* số lượng assumption;
* số lượng open question;
* số lượng yêu cầu dự kiến chuyển sang SRS;
* các vấn đề cần xác nhận;
* xác nhận file Word đã được lưu đúng đường dẫn.
