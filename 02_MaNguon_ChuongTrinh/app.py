import streamlit as st
import sqlite3
import datetime
import json
import io
import os
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from dotenv import load_dotenv
from typing import TypedDict

class TransactionSchema(TypedDict):
    type: str
    amount: int
    category: str
    description: str

load_dotenv(override=True)

st.set_page_config(
    page_title="Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "chi_tieu.db"

STUDENT_CATEGORIES = [
    "Ăn uống & Cafe",
    "Tiền nhà & Tiện ích",
    "Học tập & Sách vở",
    "Di chuyển & Xăng xe",
    "Giải trí & Bè bạn",
    "Mua sắm cá nhân",
    "Chu cấp gia đình",
    "Đi làm thêm",
    "Khác"
]

def get_db_connection():
    """Tạo kết nối tới CSDL SQLite"""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo cấu trúc cơ sở dữ liệu và nạp dữ liệu mẫu ban đầu"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS giao_dich (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loai TEXT NOT NULL,
            so_tien REAL NOT NULL,
            danh_muc TEXT NOT NULL,
            ngay TEXT NOT NULL,
            ghi_chu TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS han_muc (
            danh_muc TEXT PRIMARY KEY,
            so_tien_limit REAL NOT NULL
        )
    """)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM giao_dich")
    if cursor.fetchone()[0] == 0:
        today = datetime.date.today()
        sample_transactions = [
            ("Thu", 4000000, "Chu cấp gia đình", today.strftime("%Y-%m-01"), "Bố mẹ gửi tiền tháng này 💰"),
            ("Thu", 2500000, "Đi làm thêm", today.strftime("%Y-%m-05"), "Lương gia sư / quán cafe 💼"),
            ("Chi", 1800000, "Tiền nhà & Tiện ích", today.strftime("%Y-%m-02"), "Tiền phòng trọ & điện nước 🏠"),
            ("Chi", 1500000, "Ăn uống & Cafe", today.strftime("%Y-%m-03"), "Cơm tháng, ăn vặt & cafe chạy deadline 🍜"),
            ("Chi", 450000, "Học tập & Sách vở", today.strftime("%Y-%m-04"), "In giáo trình & mua tài liệu học 📚"),
            ("Chi", 300000, "Di chuyển & Xăng xe", today.strftime("%Y-%m-06"), "Đổ xăng & vé xe bus 🛵"),
            ("Chi", 350000, "Giải trí & Bè bạn", today.strftime("%Y-%m-07"), "Xem phim & ăn đồ nướng cuối tuần 🎬"),
        ]
        cursor.executemany("INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)", sample_transactions)
        
        sample_limits = [
            ("Ăn uống & Cafe", 2500000),
            ("Tiền nhà & Tiện ích", 2000000),
            ("Giải trí & Bè bạn", 800000),
            ("Học tập & Sách vở", 600000),
            ("Di chuyển & Xăng xe", 500000),
        ]
        cursor.executemany("INSERT OR REPLACE INTO han_muc (danh_muc, so_tien_limit) VALUES (?, ?)", sample_limits)
        conn.commit()
    conn.close()

init_db()

def load_data():
    """Truy vấn dữ liệu mới nhất từ CSDL SQLite và đồng bộ vào st.session_state"""
    conn = get_db_connection()
    
    df = pd.read_sql_query("SELECT id, loai, so_tien, danh_muc, ngay, ghi_chu FROM giao_dich ORDER BY ngay DESC, id DESC", conn)
    st.session_state["df_transactions"] = df
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN loai = 'Thu' THEN so_tien ELSE 0 END) as tong_thu,
            SUM(CASE WHEN loai = 'Chi' THEN so_tien ELSE 0 END) as tong_chi
        FROM giao_dich
    """)
    row = cursor.fetchone()
    tong_thu = row['tong_thu'] if row and row['tong_thu'] else 0.0
    tong_chi = row['tong_chi'] if row and row['tong_chi'] else 0.0
    st.session_state["summary"] = {
        "tong_thu": tong_thu,
        "tong_chi": tong_chi,
        "so_du": tong_thu - tong_chi
    }
    
    cursor.execute("SELECT danh_muc, so_tien_limit FROM han_muc")
    st.session_state["budget_limits"] = {r["danh_muc"]: r["so_tien_limit"] for r in cursor.fetchall()}
    
    conn.close()

if "df_transactions" not in st.session_state:
    load_data()

def add_transaction(loai, so_tien, danh_muc, ngay, ghi_chu):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
        (loai, so_tien, danh_muc, ngay, ghi_chu)
    )
    conn.commit()
    conn.close()
    
    st.session_state["toast_msg"] = f"✅ Đã thêm giao dịch: {loai} {so_tien:,.0f} ₫ ({danh_muc})"
    load_data()
    st.rerun()

def update_transaction(id_gd, loai, so_tien, danh_muc, ngay, ghi_chu):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE giao_dich SET loai = ?, so_tien = ?, danh_muc = ?, ngay = ?, ghi_chu = ? WHERE id = ?",
        (loai, so_tien, danh_muc, ngay, ghi_chu, id_gd)
    )
    conn.commit()
    conn.close()
    
    st.session_state["toast_msg"] = f"✏️ Đã cập nhật thành công giao dịch ID #{id_gd}!"
    load_data()
    st.rerun()

def delete_transaction(id_gd):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM giao_dich WHERE id = ?", (id_gd,))
    conn.commit()
    conn.close()
    
    st.session_state["toast_msg"] = f"🗑️ Đã xóa thành công giao dịch ID #{id_gd}!"
    load_data()
    st.rerun()

def set_budget_limit(danh_muc, limit_val):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO han_muc (danh_muc, so_tien_limit) VALUES (?, ?)", (danh_muc, limit_val))
    conn.commit()
    conn.close()
    
    st.session_state["toast_msg"] = f"🎯 Đã đặt hạn mức '{danh_muc}': {limit_val:,.0f} ₫"
    load_data()
    st.rerun()

def get_api_key():
    """Lấy API Key bảo mật, không hardcode và tránh lỗi StreamlitSecretNotFoundError"""
    load_dotenv(override=True)
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key.strip()
    
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            secrets_key = st.secrets["GEMINI_API_KEY"]
            if secrets_key:
                return secrets_key.strip()
    except Exception:
        pass
        
    return ""

GEO_BLOCK_MSG = (
    "🌐 **Hệ thống đang bị chặn địa lý (Geo-blocking).**\n\n"
    "Google Gemini API không khả dụng tại vị trí hiện tại của bạn.\n\n"
    "**Cách khắc phục:**\n"
    "1. Bật **VPN** (kết nối tới US/Singapore/Japan)\n"
    "2. Hoặc cấu hình proxy trong file `.env`:\n"
    "```\nHTTP_PROXY=http://your-proxy:port\nHTTPS_PROXY=http://your-proxy:port\n```\n"
    "3. Khởi động lại ứng dụng sau khi cấu hình."
)

def _is_geo_blocked_error(error):
    """Kiểm tra xem lỗi có phải do Geo-blocking hay không"""
    error_str = str(error).lower()
    return ("location is not supported" in error_str or
            "failed_precondition" in error_str or
            "user location" in error_str)

def _inject_proxy():
    """Đọc proxy từ biến môi trường và inject vào os.environ trước khi gọi API"""
    load_dotenv(override=True)
    http_proxy = os.getenv("HTTP_PROXY", "").strip()
    https_proxy = os.getenv("HTTPS_PROXY", "").strip()
    
    if http_proxy:
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["http_proxy"] = http_proxy
    if https_proxy:
        os.environ["HTTPS_PROXY"] = https_proxy
        os.environ["https_proxy"] = https_proxy

def init_gemini():
    """Cấu hình thư viện Gemini API với hỗ trợ Proxy tự động"""
    api_key = get_api_key()
    if not api_key:
        return False
    try:
        _inject_proxy()
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        if _is_geo_blocked_error(e):
            st.error(GEO_BLOCK_MSG)
        else:
            st.error(f"Lỗi cấu hình Gemini API: {e}")
        return False

def check_ai_key():
    """Kiểm tra xem API key đã cấu hình chưa"""
    if not get_api_key():
        st.warning("⚠️ Vui lòng cấu hình Google Gemini API Key trong file .env hoặc Secrets để sử dụng tính năng này!")
        return False
    return True

def analyze_natural_language_expense(prompt_input, summary_info=None, budget_limits=None):
    """Sử dụng Gemini API để bóc tách giao dịch VÀ phân tích tác động tài chính, lời khuyên, hệ lụy cho sinh viên"""
    if not init_gemini():
        return None
        
    ctx_thu = summary_info.get("tong_thu", 0) if summary_info else 0
    ctx_chi = summary_info.get("tong_chi", 0) if summary_info else 0
    ctx_so_du = summary_info.get("so_du", 0) if summary_info else 0
    limits_str = json.dumps(budget_limits, ensure_ascii=False) if budget_limits else "Chưa đặt"

    try:
        system_prompt = (
            "[Instructions]\n"
            "Bạn là Chuyên gia Cố vấn Quản lý Tài chính Sinh Viên AI. Hãy thực hiện bóc tách giao dịch từ câu nói người dùng, phân tích mức độ rủi ro, tác động ví, gợi ý định mức sinh viên và tư tưởng/hệ lụy tài chính.\n\n"
            "[Context]\n"
            "- Người dùng là sinh viên đại học quản lý ví cá nhân.\n"
            f"- Bối cảnh tài chính tháng hiện tại: Thu nhập {ctx_thu:,.0f} VNĐ, Đã chi {ctx_chi:,.0f} VNĐ, Số dư ví {ctx_so_du:,.0f} VNĐ.\n"
            f"- Hạn mức danh mục: {limits_str}.\n\n"
            "[Input Data / Constraints]\n"
            "1. amount: Số nguyên VNĐ (> 0). Quy đổi từ lóng ('199k' -> 199000, '5 củ' -> 5000000). Nếu có nhiều khoản chi/thu trong câu ('sáng 199k chiều 5 củ'), cộng tổng tất cả lại.\n"
            "2. type: 'chi' hoặc 'thu'.\n"
            "3. category: Chọn đúng 1 trong các danh mục sinh viên: 'Ăn uống & Cafe', 'Di chuyển', 'Giải trí', 'Mua sắm', 'Hóa đơn', 'Khác'.\n"
            "4. warning_level: 'SAFE' (chi tiêu hợp lý), 'WARNING' (chi phí hơi cao), 'CRITICAL' (vượt hạn mức / sụt giảm nghiêm trọng số dư / xa xỉ đối với sinh viên).\n"
            "5. Đầy đủ các trường: type, amount, category, description, warning_level, financial_impact, smart_advice, consequences.\n\n"
            "[Examples / Few-Shot]\n"
            "- Input: 'Sáng ăn phở 30k trưa cafe 40k'\n"
            "  Output: { \"type\": \"chi\", \"amount\": 70000, \"category\": \"Ăn uống & Cafe\", \"description\": \"Ăn sáng phở và uống cafe trưa\", \"warning_level\": \"SAFE\", \"financial_impact\": \"Chi 70.000 VNĐ chiếm 1.4% số dư hiện tại\", \"smart_advice\": \"Mức chi tiêu hợp lý cho sinh viên\", \"consequences\": \"Duy trì mức ăn uống này sẽ giữ ví an toàn đến cuối tháng.\" }\n\n"
            "[Chain-of-Thought Reasoning]\n"
            "- Bước 1: Trích xuất các khoản số tiền & từ lóng, cộng dồn tổng tiền.\n"
            "- Bước 2: Phân loại Thu/Chi và gán danh mục phù hợp nhất.\n"
            "- Bước 3: So sánh khoản chi với Số Dư Ví & Hạn Mức để xếp hạng warning_level.\n"
            "- Bước 4: Soạn nội dung tư vấn tác động tài chính và định hình tư tưởng tài chính chuẩn sinh viên.\n\n"
            "[Output Format]\n"
            "JSON Object duy nhất chuẩn định dạng 8 trường trên."
        )
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
        
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_prompt,
            generation_config=generation_config
        )
        
        response = model.generate_content(prompt_input)
        parsed = json.loads(response.text)

        if isinstance(parsed, list):
            if len(parsed) > 0 and isinstance(parsed[0], dict):
                first_item = parsed[0]
                total_amt = sum(float(item.get("amount", 0)) for item in parsed if isinstance(item, dict))
                first_item["amount"] = total_amt
                return first_item
            return None
        elif isinstance(parsed, dict):
            return parsed
        return None
    except Exception as e:
        if _is_geo_blocked_error(e):
            st.error(GEO_BLOCK_MSG)
        else:
            st.error(f"❌ Lỗi xử lý từ Gemini API: {e}")
        return None

def generate_savings_advice(df_transactions):
    """Sử dụng Gemini để đưa ra nhận xét, lời khuyên quản lý ngân sách sinh viên"""
    if not init_gemini():
        return "Chưa cấu hình API Key thích hợp."
        
    try:
        system_prompt = (
            "[Instructions]\n"
            "Bạn là Chuyên gia Cố vấn Quản lý Tài chính Sinh Viên & Giải Toán AI. Phân tích lịch sử chi tiêu từ dữ liệu CSV và đưa ra lời khuyên tiết kiệm súc tích, mạch lạc.\n\n"
            "[Context]\n"
            "- Hệ thống hỗ trợ quản lý ví sinh viên.\n"
            "- Phạm vi cho phép (Allowlist): 1. Quản lý tài chính & tiết kiệm; 2. Toán học & tư duy logic.\n"
            "- Phạm vi từ chối (Denylist): Tất cả các chủ đề ngoài tài chính & toán học (lịch sử, nấu ăn, tán tán phiếm...).\n\n"
            "[Constraints / Rules]\n"
            "- Khi nằm trong chuyên môn: Trả lời ngắn gọn, có gạch đầu dòng, nêu rõ tỷ lệ % khoản chi chiếm nhiều nhất.\n"
            "- Khi ngoài chuyên môn: Bắt buộc từ chối bằng đúng mẫu câu:\n"
            "  '⛔ Xin lỗi, tôi là trợ lý AI chuyên biệt. Tôi chỉ có thể hỗ trợ bạn các vấn đề liên quan đến **Tài chính - Chi tiêu** và **Toán học**. Vui lòng đặt câu hỏi đúng chuyên môn!'\n\n"
            "[Output Format]\n"
            "Markdown trình bày đẹp mắt với các gạch đầu dòng phân tích & lời khuyên hành động."
        )
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,
        )
        
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_prompt,
            generation_config=generation_config
        )
        
        summary_str = df_transactions.to_csv(index=False)
        prompt = f"Dưới đây là danh sách thu chi cá nhân dạng CSV của một sinh viên:\n\n{summary_str}\n\nHãy phân tích và đưa ra lời khuyên tiết kiệm súc tích."
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if _is_geo_blocked_error(e):
            return GEO_BLOCK_MSG
        return f"❌ Lỗi kết nối Gemini API: {e}"

def chat_with_gemini(chat_history, user_query, df_transactions):
    """Thực hiện hội thoại liên tục với Gemini chatbot, tích hợp dữ liệu chi tiêu hiện tại"""
    if not init_gemini():
        return None
        
    try:
        ctx_summary = df_transactions.to_string(index=False) if not df_transactions.empty else "Chưa có dữ liệu giao dịch."
        
        system_instruction = (
            "[Instructions]\n"
            "Bạn là Trợ lý AI Sinh Viên Gemini chuyên biệt trong 2 lĩnh vực: QUẢN LÝ TÀI CHÍNH & GIẢI TOÁN HỌC.\n\n"
            "[Context]\n"
            "- Người dùng là sinh viên hỏi đáp thắc mắc chi tiêu hoặc bài tập toán.\n"
            f"- Dữ liệu thu chi ví hiện tại của sinh viên:\n{ctx_summary}\n\n"
            "[Constraints / Allowlist & Denylist]\n"
            "- ALLOWLIST: Quản lý tài chính, mẹo tiết kiệm sinh viên, giải bài tập toán học từ cơ bản tới cao cấp.\n"
            "- DENYLIST: Hỏi chuyện phiếm, lịch sử, địa lý, chính trị, viết thư, giải trí khác.\n"
            "- Khi bị hỏi ngoài chuyên môn: Trả lời duy nhất câu từ chối chuẩn:\n"
            "  '⛔ Xin lỗi, tôi là trợ lý AI chuyên biệt. Tôi chỉ có thể hỗ trợ bạn các vấn đề liên quan đến **Tài chính - Chi tiêu** và **Toán học**. Vui lòng đặt câu hỏi đúng chuyên môn!'\n\n"
            "[Output Format]\n"
            "Trả lời dạng Markdown súc tích, mạch lạc, chính xác."
        )
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,
        )
        
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction,
            generation_config=generation_config
        )
        
        gemini_history = []
        for msg in chat_history[1:]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
            
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_query)
        return response.text
    except Exception as e:
        if _is_geo_blocked_error(e):
            st.error(GEO_BLOCK_MSG)
        else:
            st.error(f"❌ Lỗi kết nối Gemini API: {e}")
        return None

def chat_with_gemini_agent(user_query, df_transactions, summary, budget_limits):
    """Trợ lý CSKH Gemini Agentic: Nhận diện ý định điều khiển ứng dụng và trả về JSON hành động"""
    if not init_gemini():
        return {"action": "CHAT", "reply": "Chưa cấu hình Gemini API Key."}
        
    ctx_summary = df_transactions.to_string(index=False) if not df_transactions.empty else "Chưa có dữ liệu giao dịch."
    limits_str = json.dumps(budget_limits, ensure_ascii=False) if budget_limits else "Chưa đặt"

    system_instruction = (
        "[Instructions]\n"
        "Bạn là Trợ Lý CSKH & Cố Vấn Điều Hành AI của Sổ Tay Sinh Viên 🎓. Bạn có quyền THỰC THI TRỰC TIẾP các hành động hệ thống (Thêm khoản chi/thu, xóa giao dịch, đặt hạn mức) hoặc tư vấn chat.\n\n"
        "[Context]\n"
        "- Hệ thống hỗ trợ sinh viên quản lý tài chính và điều hành ứng dụng qua giọng nói/ngôn ngữ tự nhiên.\n"
        f"- Thống kê ví hiện tại: Thu {summary.get('tong_thu',0):,.0f} ₫ | Chi {summary.get('tong_chi',0):,.0f} ₫ | Số dư {summary.get('so_du',0):,.0f} ₫\n"
        f"- Hạn mức ngân sách: {limits_str}\n"
        f"- Danh sách giao dịch mới nhất:\n{ctx_summary}\n\n"
        "[Input Data / Action Definitions]\n"
        "1. ADD_TRANSACTION: Thêm thu/chi tự động (loai, so_tien, danh_muc, ghi_chu, reply)\n"
        "2. DELETE_TRANSACTION: Xóa giao dịch theo ID (id, reply)\n"
        "3. SET_BUDGET: Đặt hạn mức chi tiêu (danh_muc, limit_val, reply)\n"
        "4. CHAT: Trả lời tư vấn / hỏi đáp chung (reply)\n\n"
        "[Examples / Few-Shot]\n"
        "- User: 'Thêm chi phở 35k'\n"
        "  JSON: {\"action\": \"ADD_TRANSACTION\", \"loai\": \"Chi\", \"so_tien\": 35000, \"danh_muc\": \"Ăn uống & Cafe\", \"ghi_chu\": \"Ăn phở\", \"reply\": \"Dạ em đã thêm khoản chi phở 35.000 ₫ cho mình rồi ạ! 🍜\"}\n"
        "- User: 'Xóa giao dịch 4'\n"
        "  JSON: {\"action\": \"DELETE_TRANSACTION\", \"id\": 4, \"reply\": \"Dạ em đã xóa thành công giao dịch ID #4 cho mình ạ! 🗑️\"}\n"
        "- User: 'Đặt hạn mức giải trí 500k'\n"
        "  JSON: {\"action\": \"SET_BUDGET\", \"danh_muc\": \"Giải trí & Bè bạn\", \"limit_val\": 500000, \"reply\": \"Dạ em đã cập nhật hạn mức Giải trí & Bè bạn là 500.000 ₫ rồi ạ! 🎯\"}\n\n"
        "[Output Format]\n"
        "Bắt buộc trả về đúng 1 JSON Object duy nhất chứa trường 'action' và các trường tương ứng."
    )

    generation_config = genai.types.GenerationConfig(
        temperature=0.2,
        response_mime_type="application/json"
    )

    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction,
            generation_config=generation_config
        )

        response = model.generate_content(user_query)
        parsed = json.loads(response.text)
        if isinstance(parsed, list) and len(parsed) > 0:
            parsed = parsed[0]
        return parsed
    except Exception as e:
        if _is_geo_blocked_error(e):
            return {"action": "CHAT", "reply": GEO_BLOCK_MSG}
        return {"action": "CHAT", "reply": f"Dạ em là Trợ lý CSKH, rất tiếc có lỗi kết nối: {e}"}

def draw_pie_chart(df_all):
    """Vẽ biểu đồ tròn hiển thị danh mục chi tiêu nhiều nhất"""
    df_chi = df_all[df_all["loai"] == "Chi"]
    if not df_chi.empty:
        cat_summary = df_chi.groupby("danh_muc")["so_tien"].sum().reset_index()
        STUDENT_PALETTE = ['#0EA5E9', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#64748B']
        
        fig_pie = px.pie(
            cat_summary, 
            values="so_tien", 
            names="danh_muc", 
            hole=0.45,
            color_discrete_sequence=STUDENT_PALETTE
        )
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label', 
            marker=dict(line=dict(width=2))
        )
        fig_pie.update_layout(
            margin=dict(t=30, b=30, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit")
    else:
        st.info("Chưa có dữ liệu chi tiêu để vẽ biểu đồ phân phối.")

def draw_bar_chart(df_all):
    """Vẽ biểu đồ cột so sánh tổng Thu vs tổng Chi theo từng tháng"""
    df_all_copy = df_all.copy()
    df_all_copy["thang"] = pd.to_datetime(df_all_copy["ngay"]).dt.strftime("%Y-%m")
    monthly_summary = df_all_copy.groupby(["thang", "loai"])["so_tien"].sum().reset_index()
    
    fig_bar = px.bar(
        monthly_summary,
        x="thang",
        y="so_tien",
        color="loai",
        barmode="group",
        color_discrete_map={"Thu": "#10B981", "Chi": "#EF4444"},
        labels={"so_tien": "Số tiền (VND)", "thang": "Tháng"}
    )
    fig_bar.update_layout(
        margin=dict(t=30, b=30, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit")

def draw_line_chart(df_all):
    """Vẽ biểu đồ đường xu hướng chi tiêu theo ngày trong tháng hiện tại"""
    df_chi = df_all[df_all["loai"] == "Chi"].copy()
    if df_chi.empty:
        st.info("Chưa có dữ liệu chi tiêu để vẽ biểu đồ xu hướng.")
        return
    
    current_month = datetime.date.today().strftime("%Y-%m")
    df_chi["ngay_dt"] = pd.to_datetime(df_chi["ngay"])
    df_month = df_chi[df_chi["ngay_dt"].dt.strftime("%Y-%m") == current_month]
    
    if df_month.empty:
        st.info("Chưa có dữ liệu chi tiêu tháng này.")
        return
    
    daily = df_month.groupby(df_month["ngay_dt"].dt.date)["so_tien"].sum().reset_index()
    daily.columns = ["Ngày", "Tổng chi"]
    daily = daily.sort_values("Ngày")
    daily["Tích lũy"] = daily["Tổng chi"].cumsum()
    
    fig_line = px.line(
        daily,
        x="Ngày",
        y="Tích lũy",
        markers=True,
        labels={"Tích lũy": "Chi tiêu tích lũy (VND)", "Ngày": ""},
        color_discrete_sequence=["#0EA5E9"]
    )
    fig_line.add_bar(
        x=daily["Ngày"],
        y=daily["Tổng chi"],
        name="Chi tiêu/ngày",
        marker_color="rgba(239, 68, 68, 0.4)"
    )
    fig_line.update_layout(
        margin=dict(t=30, b=30, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_line, use_container_width=True, theme="streamlit")

def inject_custom_css():
    """Đưa CSS tùy biến vào Streamlit, sử dụng hoàn toàn CSS variables + micro-animations"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* ============ CLEAN UP DEFAULT STREAMLIT MENU & FOOTER ============ */
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        header { visibility: hidden !important; }

        /* ============ GLOBAL FONT & BASE TYPOGRAPHY ============ */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Plus Jakarta Sans', 'Roboto', 'Segoe UI', sans-serif !important;
        }

        .stApp {
            background-color: #f4f7f6 !important;
            color: #1f2937 !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #1f2937 !important;
            margin-bottom: 0.8rem !important;
            font-weight: 700 !important;
        }

        /* ============ FADE-IN ANIMATION ============ */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stTabs, div[data-testid="stMetric"], .stForm, .stPlotlyChart {
            animation: fadeInUp 0.4s ease-out both;
        }

        /* ============ PIXEL-PERFECT SIDEBAR SAAS OPTIMIZATION ============ */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            box-shadow: 4px 0 15px rgba(0, 0, 0, 0.03) !important;
            border-right: 1px solid #e2e8f0 !important;
        }

        [data-testid="stSidebar"] .block-container {
            padding: 1.5rem 24px !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.5) !important;
        }

        [data-testid="stSidebar"] [data-testid="stAlert"], [data-testid="stSidebar"] .stAlert {
            background-color: #ecfdf5 !important;
            border-left: 4px solid #10b981 !important;
            color: #065f46 !important;
            border-radius: 6px !important;
            border-top: none !important;
            border-right: none !important;
            border-bottom: none !important;
        }

        [data-testid="stSidebar"] hr {
            border-top: 1px dashed #e2e8f0 !important;
            border-bottom: none !important;
            border-left: none !important;
            border-right: none !important;
            margin: 1.5rem 0 !important;
        }

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] caption {
            color: #64748b !important;
            font-size: 0.85rem !important;
        }

        /* ============ SIDEBAR HEADER GLASSMORPHISM & COLLAPSE BUTTON ============ */
        [data-testid="stSidebarHeader"] {
            background: rgba(248, 250, 252, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            padding: 1rem 1.5rem 0.5rem 1.5rem !important;
            border-bottom: 1px solid rgba(0, 0, 0, 0.04) !important;
        }

        [data-testid="stSidebarHeader"] button, [data-testid="stSidebarCollapseButton"] button {
            background-color: #ffffff !important;
            border-radius: 50% !important;
            border: 1px solid #e2e8f0 !important;
            width: 32px !important;
            height: 32px !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            color: #64748b !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stSidebarHeader"] button:hover, [data-testid="stSidebarCollapseButton"] button:hover {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
            transform: scale(1.05) !important;
        }

        [data-testid="stSidebar"] img, [data-testid="stSidebarHeader"] img {
            filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.12)) !important;
            transition: transform 0.3s ease !important;
        }

        [data-testid="stSidebar"] img:hover, [data-testid="stSidebarHeader"] img:hover {
            transform: translateY(-3px) !important;
        }

        /* ============ GRADIENT HEADER ============ */
        .student-header {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 50%, #10B981 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
            margin-bottom: 0.2rem;
        }

        /* ============ SAAS CARD UI & HOVER ANIMATIONS ============ */
        div[data-testid="stMetric"], .stPlotlyChart, .stAltairChart, .stForm, .health-card {
            background: #ffffff !important;
            border: 1px solid rgba(226, 232, 240, 0.8) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }

        div[data-testid="stMetric"]:hover, .stPlotlyChart:hover, .stForm:hover, .health-card:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
        }

        div[data-testid="stMetricLabel"] > div {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            color: #64748b !important;
        }

        div[data-testid="stMetricValue"] > div {
            font-size: 1.8rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
        }

        /* ============ MODERN SEGMENTED CONTROL TABS ============ */
        [data-baseweb="tab-list"] {
            background-color: #f1f5f9 !important;
            border-radius: 12px !important;
            padding: 6px !important;
            gap: 8px !important;
            border-bottom: none !important;
        }

        [data-baseweb="tab"] {
            background-color: transparent !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            color: #64748b !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }

        [data-baseweb="tab"]:hover {
            color: #1f2937 !important;
            background-color: #e2e8f0 !important;
        }

        [data-baseweb="tab"][aria-selected="true"] {
            background-color: #ffffff !important;
            color: #4f46e5 !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        }

        [data-baseweb="tab-highlight"] {
            display: none !important;
        }

        /* ============ FORM INPUTS & FOCUS MICRO-INTERACTIONS ============ */
        .stTextInput input, .stNumberInput input, .stSelectbox > div > div, .stDateInput input {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 10px !important;
            color: #0f172a !important;
            font-weight: 500 !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus,
        .stTextInput:focus-within input, .stNumberInput:focus-within input, .stSelectbox:focus-within > div > div {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
            outline: none !important;
        }

        /* ============ BUTTONS WITH CLICK ANIMATION ============ */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25) !important;
            transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35) !important;
        }

        .stButton > button:active {
            transform: scale(0.97) !important;
        }

        /* ============ GLOBAL SAAS SCROLLBAR OPTIMIZATION ============ */
        * {
            scrollbar-width: thin !important;
            scrollbar-color: #cbd5e1 transparent !important;
        }

        ::-webkit-scrollbar {
            width: 6px !important;
            height: 6px !important;
        }

        ::-webkit-scrollbar-track {
            background: transparent !important;
            border-radius: 10px !important;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e1 !important;
            border-radius: 10px !important;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8 !important;
        }

        /* DATAFRAME & TABLE SCROLLBAR HARMONIZATION */
        [data-testid="stDataFrame"] div, [data-testid="stTable"] div {
            scrollbar-width: thin !important;
            scrollbar-color: #cbd5e1 transparent !important;
        }

        /* ============ PROGRESS BAR ROUNDED TRACK & FILL ============ */
        .stProgress > div {
            border-radius: 10px !important;
        }
        .stProgress > div > div {
            border-radius: 10px !important;
        }

        /* ============ HEALTH SCORE CARD ============ */
        .health-card {
            padding: 18px;
            border-radius: 16px;
            background: #ffffff;
            margin-bottom: 12px;
            text-align: center;
        }
        .health-score {
            font-size: 2rem;
            font-weight: 800;
            margin: 4px 0;
        }
        .health-label {
            font-size: 0.85rem;
            color: #64748b;
        }

        /* ============ PERFECT CIRCULAR FLOATING ACTION BUTTON (FAB) ============ */
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            z-index: 999999 !important;
        }

        div[data-testid="stPopover"] > button {
            border-radius: 50% !important;
            width: 60px !important;
            height: 60px !important;
            min-width: 60px !important;
            min-height: 60px !important;
            max-width: 60px !important;
            max-height: 60px !important;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.25s ease !important;
        }

        div[data-testid="stPopover"] > button:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 12px 35px rgba(168, 85, 247, 0.8) !important;
        }

        div[data-testid="stPopover"] > button svg {
            display: none !important;
        }

        div[data-testid="stPopover"] > button p {
            font-size: 28px !important;
            margin: 0 !important;
            line-height: 1 !important;
            color: #ffffff !important;
        }

        /* ============ POP-IN ANIMATION & ENLARGED POPOVER CHAT CARD ============ */
        @keyframes popInAI {
            0% { opacity: 0; transform: scale(0.85) translateY(20px); }
            100% { opacity: 1; transform: scale(1) translateY(0); }
        }

        /* Cửa sổ chat card mở ra ghim CHUẨN GÓC DƯỚI BÊN PHẢI với hiệu ứng Pop-in */
        div[data-testid="stPopoverBody"], div[data-testid="stPopoverContent"] {
            position: fixed !important;
            bottom: 95px !important;
            right: 25px !important;
            z-index: 999999 !important;
            border-radius: 16px !important;
            border: 1px solid rgba(226, 232, 240, 0.9) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25) !important;
            padding: 18px !important;
            width: 450px !important;
            max-width: 95vw !important;
            height: 650px !important;
            max-height: 85vh !important;
            scrollbar-width: none !important;
            animation: popInAI 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
        }

        div[data-testid="stPopoverBody"]::-webkit-scrollbar, div[data-testid="stPopoverContent"]::-webkit-scrollbar {
            display: none !important;
            width: 0px !important;
            background: transparent !important;
        }

        /* Tối ưu khu vực nhập liệu Chat Input dính lề dưới */
        div[data-testid="stPopoverBody"] [data-testid="stChatInput"], 
        div[data-testid="stPopoverContent"] [data-testid="stChatInput"] {
            position: sticky !important;
            bottom: 0 !important;
            background: #ffffff !important;
            z-index: 10 !important;
            padding-top: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Hiển thị giao diện menu bên hông"""
    with st.sidebar:
        st.image("https://img.icons8.com/isometric/100/student-male.png", width=75)
        st.markdown("<h2 style='font-weight:800; font-size:1.35rem;'>🎓 Sổ Tay Sinh Viên</h2>", unsafe_allow_html=True)
        st.caption("Quản lý tài chính cá nhân thông minh & tiết kiệm")
        
        if st.button("🔄 Đồng bộ dữ liệu mới", use_container_width=True, type="secondary", key="sb_sync_btn"):
            load_data()
            st.session_state["toast_msg"] = "🔄 Đã cập nhật lại CSDL mới nhất!"
            st.rerun()

        st.markdown("---")

        if get_api_key():
            st.success("🔑 Gemini API Key: Đã được kết nối thành công từ môi trường (.env / Secrets)")
        else:
            st.error("⚠️ Gemini API Key: Chưa cấu hình. Vui lòng thêm GEMINI_API_KEY vào file .env")

        st.markdown("---")
        st.subheader("🎯 Đặt Hạn Mức Tiêu Tháng")
        selected_b_cat = st.selectbox("Chọn khoản chi", STUDENT_CATEGORIES[:6], key="sb_budget_cat")
        b_limit_val = st.number_input("Hạn mức tối đa (VND)", min_value=100000.0, step=100000.0, value=2000000.0, format="%.0f", key="sb_budget_val")
        if st.button("💾 Đặt Hạn Mức", type="primary", use_container_width=True, key="sb_save_limit_btn"):
            set_budget_limit(selected_b_cat, b_limit_val)

        st.markdown("---")
        st.subheader("💚 Sức Khỏe Tài Chính")
        sb_summary = st.session_state.get("summary", {"tong_thu": 0, "tong_chi": 0, "so_du": 0})
        sb_thu = sb_summary["tong_thu"]
        sb_chi = sb_summary["tong_chi"]
        if sb_thu > 0:
            saving_rate = ((sb_thu - sb_chi) / sb_thu) * 100
        else:
            saving_rate = 0
        
        if saving_rate >= 20:
            score_color = "#10B981"
            score_label = "Tuyệt vời! 🌟"
        elif saving_rate >= 10:
            score_color = "#F59E0B"
            score_label = "Tạm ổn 👍"
        elif saving_rate >= 0:
            score_color = "#EF4444"
            score_label = "Cần cải thiện ⚠️"
        else:
            score_color = "#DC2626"
            score_label = "Cháy túi! 🔥"
        
        st.markdown(f"""
            <div class="health-card">
                <div class="health-label">Tỷ lệ tiết kiệm</div>
                <div class="health-score" style="color: {score_color}">{saving_rate:.1f}%</div>
                <div class="health-label">{score_label}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if sb_thu > 0:
            st.progress(min(max(saving_rate / 100, 0), 1.0))
        st.caption(f"Thu: {sb_thu:,.0f} ₫ | Chi: {sb_chi:,.0f} ₫")

def render_floating_cskh_widget(df_all, summary, budget_limits):
    """Hiển thị Nút Tròn CSKH Nổi ở góc dưới bên phải màn hình (Bottom-Right Viewport Fixed Button)"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Chào bạn! Mình là **Trợ Lý CSKH AI 🎓**. Bạn cần mình thực hiện thao tác gì (Thêm/Xóa/Hạn mức) hay hỗ trợ điều gì không?"}
        ]

    with st.container():
        with st.popover("🤖", help="Mở Trợ Lý Gemini AI 🎓"):
            st.markdown("### 💬 Trợ Lý CSKH & Điều Hành AI 🎓")
            st.caption("Thực thi mọi thao tác: Thêm khoản chi, xóa giao dịch, đặt hạn mức, tư vấn tiết kiệm...")
            
            if st.button("🗑️ Xóa Lịch Sử CSKH", key="clear_cskh_pop_btn", type="secondary", use_container_width=True):
                st.session_state.messages = [
                    {"role": "assistant", "content": "👋 Chào bạn! Mình là **Trợ Lý CSKH AI 🎓**. Bạn cần mình thực hiện thao tác gì (Thêm/Xóa/Hạn mức) hay hỗ trợ điều gì không?"}
                ]
                st.rerun()

            chat_container = st.container(height=300)
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            pop_user_input = st.chat_input("Nhập yêu cầu CSKH...", key="pop_cskh_chat_input")
            if pop_user_input:
                st.session_state.messages.append({"role": "user", "content": pop_user_input})
                
                if check_ai_key():
                    with st.spinner("Trợ lý CSKH AI đang thực thi..."):
                        agent_res = chat_with_gemini_agent(pop_user_input, df_all, summary, budget_limits)
                        if agent_res:
                            action = agent_res.get("action", "CHAT")
                            reply_text = agent_res.get("reply", "Dạ em đã ghi nhận.")

                            if action == "ADD_TRANSACTION":
                                loai = agent_res.get("loai", "Chi")
                                amt = float(agent_res.get("so_tien", 0))
                                cat = agent_res.get("danh_muc", "Khác")
                                note = agent_res.get("ghi_chu", pop_user_input)
                                today = datetime.date.today().strftime("%Y-%m-%d")
                                if amt > 0:
                                    add_transaction(loai, amt, cat, today, note)

                            elif action == "DELETE_TRANSACTION":
                                del_id = int(agent_res.get("id", 0))
                                if del_id > 0:
                                    delete_transaction(del_id)

                            elif action == "SET_BUDGET":
                                b_cat = agent_res.get("danh_muc", "Khác")
                                b_lim = float(agent_res.get("limit_val", 0))
                                if b_lim > 0:
                                    set_budget_limit(b_cat, b_lim)

                            st.session_state.messages.append({"role": "assistant", "content": reply_text})
                            st.rerun()

def render_header():
    """Hiển thị thanh tiêu đề và các thông điệp phản hồi nhanh"""
    header_col1, header_col2 = st.columns([0.8, 0.2])
    with header_col1:
        st.markdown('<div class="student-header">🎓 QUẢN LÝ CHI TIÊU SINH VIÊN AI</div>', unsafe_allow_html=True)
        st.caption("Sổ tay quản lý ví sinh viên thông minh 🍜 Đồng hành cùng bạn vượt qua mùa deadline và tránh nguy cơ cháy túi nhờ Trợ lý AI Gemini")
    with header_col2:
        if st.button("🔄 Làm mới dữ liệu", key="header_refresh", type="secondary"):
            load_data()
            st.session_state["toast_msg"] = "🔄 Dữ liệu ví sinh viên đã được đồng bộ mới nhất!"
            st.rerun()

    if "toast_msg" in st.session_state and st.session_state["toast_msg"]:
        st.toast(st.session_state.pop("toast_msg"), icon="🎒")

def main():
    inject_custom_css()
    
    render_sidebar()
    render_header()
    
    df_all = st.session_state.get("df_transactions", pd.DataFrame())
    summary = st.session_state.get("summary", {"tong_thu": 0.0, "tong_chi": 0.0, "so_du": 0.0})
    budget_limits = st.session_state.get("budget_limits", {})
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Thống Kê", 
        "➕ Thêm Chi Tiêu", 
        "📜 Lịch Sử", 
        "🧠 Gợi Ý Tiết Kiệm"
    ])

    with tab1:
        tong_thu = summary["tong_thu"]
        tong_chi = summary["tong_chi"]
        so_du = summary["so_du"]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🟢 Tổng Tiền Nhận (Thu)", f"{tong_thu:,.0f} ₫")
        col2.metric("🔴 Tổng Tiền Tiêu (Chi)", f"{tong_chi:,.0f} ₫")
        
        delta_color = "normal" if so_du >= 0 else "inverse"
        col3.metric(
            "💰 Số Dư Ví Sinh Viên", 
            f"{so_du:,.0f} ₫", 
            delta=f"{so_du:,.0f} ₫" if so_du >= 0 else "Cảnh báo hết tiền!", 
            delta_color=delta_color
        )

        if so_du < 0:
            st.error("⚠️ **CẢNH BÁO CHÁY TÚI**: Bạn đã tiêu vượt số tiền hiện có! Hãy ăn cơm KTX hoặc thắt chặt chi tiêu gấp 🍜")
        elif 0 < so_du < 500000:
            st.warning("⚡ **CẢNH BÁO BÁO ĐỘNG**: Số dư ví chỉ còn dưới 500.000 ₫! Hãy tiết kiệm cho những ngày còn lại của tháng.")

        if not df_all.empty:
            df_all_copy = df_all.copy()
            df_all_copy["ngay_dt"] = pd.to_datetime(df_all_copy["ngay"])
            current_m = datetime.date.today().strftime("%Y-%m")
            prev_m = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")
            
            chi_this = df_all_copy[(df_all_copy["loai"] == "Chi") & (df_all_copy["ngay_dt"].dt.strftime("%Y-%m") == current_m)]["so_tien"].sum()
            chi_prev = df_all_copy[(df_all_copy["loai"] == "Chi") & (df_all_copy["ngay_dt"].dt.strftime("%Y-%m") == prev_m)]["so_tien"].sum()
            thu_this = df_all_copy[(df_all_copy["loai"] == "Thu") & (df_all_copy["ngay_dt"].dt.strftime("%Y-%m") == current_m)]["so_tien"].sum()
            thu_prev = df_all_copy[(df_all_copy["loai"] == "Thu") & (df_all_copy["ngay_dt"].dt.strftime("%Y-%m") == prev_m)]["so_tien"].sum()
            
            cmp_c1, cmp_c2 = st.columns(2)
            with cmp_c1:
                chi_delta = chi_this - chi_prev
                chi_delta_pct = f"{(chi_delta / chi_prev * 100):+.1f}%" if chi_prev > 0 else "N/A"
                st.metric(
                    f"🔴 Chi Tiêu Tháng {current_m}",
                    f"{chi_this:,.0f} ₫",
                    delta=f"{chi_delta:+,.0f} ₫ ({chi_delta_pct}) so với tháng trước",
                    delta_color="inverse"
                )
            with cmp_c2:
                thu_delta = thu_this - thu_prev
                thu_delta_pct = f"{(thu_delta / thu_prev * 100):+.1f}%" if thu_prev > 0 else "N/A"
                st.metric(
                    f"🟢 Thu Nhập Tháng {current_m}",
                    f"{thu_this:,.0f} ₫",
                    delta=f"{thu_delta:+,.0f} ₫ ({thu_delta_pct}) so với tháng trước",
                    delta_color="normal"
                )

        st.markdown("---")
        
        st.subheader("🎯 Hạn Mức Chi Tiêu Cho Sinh Viên Tháng Này")
        if not df_all.empty:
            df_chi = df_all[df_all["loai"] == "Chi"]
            spent_by_cat = df_chi.groupby("danh_muc")["so_tien"].sum().to_dict() if not df_chi.empty else {}
            
            if budget_limits:
                b_cols = st.columns(min(len(budget_limits), 4))
                col_idx = 0
                for cat, limit_amt in budget_limits.items():
                    spent = spent_by_cat.get(cat, 0.0)
                    pct = min(spent / limit_amt, 1.0) if limit_amt > 0 else 0.0
                    
                    with b_cols[col_idx % len(b_cols)]:
                        st.markdown(f"**{cat}**")
                        st.caption(f"Đã tiêu: {spent:,.0f} / {limit_amt:,.0f} ₫ ({pct*100:.1f}%)")
                        if pct >= 1.0:
                            st.progress(pct, text="⚠️ Vượt hạn mức!")
                        elif pct >= 0.8:
                            st.progress(pct, text="⚡ Sắp chạm hạn mức")
                        else:
                            st.progress(pct)
                        col_idx += 1
            else:
                st.info("Chưa cấu hình hạn mức chi tiêu. Hãy đặt hạn mức ở thanh bên trái!")
        else:
            st.info("Chưa có chi tiêu nào được ghi nhận.")
        
        st.markdown("---")
        
        if not df_all.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🥧 Các Khoản Chi Chiếm Nhiều Tiền Nhất")
                draw_pie_chart(df_all)
            with c2:
                st.subheader("📊 Thu vs Chi Theo Tháng")
                draw_bar_chart(df_all)
            
            st.markdown("---")
            st.subheader("📈 Xu Hướng Chi Tiêu Tháng Này (Theo Ngày)")
            draw_line_chart(df_all)
        else:
            st.info("Chưa có giao dịch nào để hiển thị biểu đồ.")

    with tab2:
        chat_col1, chat_col2 = st.columns([0.75, 0.25])
        with chat_col1:
            st.subheader("🤖 Trợ Lý AI Nhập Chi Tiêu & Cố Vấn Tài Chính")
            st.caption("Gõ câu tự nhiên: 'Trưa ăn cơm bụi 30k', 'Sáng ăn 199k chiều ăn 5 củ', 'Nhận 3 triệu tiền làm thêm'...")
        with chat_col2:
            if st.button("🗑️ Xóa Lịch Sử Chat", key="clear_exp_chat_btn", type="secondary"):
                st.session_state.expense_chat_history = [
                    {"role": "assistant", "content": "Chào bạn! Mình là Trợ lý AI Bóc Tách & Cố Vấn Ví Sinh Viên 🎓. Hôm nay bạn mới tiêu khoản gì hay nhận tiền thu nhập nào không? Gõ cho mình biết nhé!"}
                ]
                if "ai_parsed_data" in st.session_state:
                    del st.session_state["ai_parsed_data"]
                st.rerun()

        if "expense_chat_history" not in st.session_state:
            st.session_state.expense_chat_history = [
                {"role": "assistant", "content": "Chào bạn! Mình là Trợ lý AI Bóc Tách & Cố Vấn Ví Sinh Viên 🎓. Hôm nay bạn mới tiêu khoản gì hay nhận tiền thu nhập nào không? Gõ cho mình biết nhé!"}
            ]

        for msg in st.session_state.expense_chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_exp_input = st.chat_input("Gõ câu chi tiêu hoặc thu nhập của bạn...", key="tab2_chat_input")
        if user_exp_input:
            st.session_state.expense_chat_history.append({"role": "user", "content": user_exp_input})
            with st.chat_message("user"):
                st.markdown(user_exp_input)

            if check_ai_key():
                with st.chat_message("assistant"):
                    with st.spinner("Trợ lý Gemini đang bóc tách số liệu & phân tích tác động ví..."):
                        result = analyze_natural_language_expense(user_exp_input, summary, budget_limits)
                        if isinstance(result, dict) and float(result.get("amount", 0)) > 0:
                            loai = "Thu" if str(result.get("type", "")).lower() == "thu" else "Chi"
                            so_tien = float(result.get("amount", 0))
                            
                            category_mapping = {
                                "Ăn uống & Cafe": "Ăn uống & Cafe",
                                "Di chuyển": "Di chuyển & Xăng xe",
                                "Giải trí": "Giải trí & Bè bạn",
                                "Mua sắm": "Mua sắm cá nhân",
                                "Hóa đơn": "Tiền nhà & Tiện ích",
                                "Khác": "Khác"
                            }
                            raw_cat = str(result.get("category", "Khác"))
                            danh_muc = category_mapping.get(raw_cat, "Khác")
                            mo_ta = str(result.get("description", user_exp_input))
                            today_str = datetime.date.today().strftime("%Y-%m-%d")
                            warning_lvl = str(result.get("warning_level", "SAFE")).upper()
                            
                            financial_impact = str(result.get("financial_impact", ""))
                            smart_advice = str(result.get("smart_advice", ""))
                            consequences = str(result.get("consequences", ""))

                            badge = "🚨 **CẢNH BÁO BÁO ĐỘNG CRITICAL**" if warning_lvl == "CRITICAL" else ("⚠️ **CẢNH BÁO CAO WARNING**" if warning_lvl == "WARNING" else "✅ **CHI TIÊU AN TOÀN SAFE**")
                            
                            ai_reply = f"""
{badge}

📌 **Bóc tách giao dịch**:
- **Loại**: {loai}
- **Số tiền**: **{so_tien:,.0f} ₫**
- **Danh mục**: {danh_muc}
- **Mô tả**: {mo_ta}

💥 **Tác Động Ví**: {financial_impact}
💡 **Gợi Ý Sinh Viên**: {smart_advice}
🔥 **Hệ Lụy & Tư Tưởng**: {consequences}
                            """
                            st.markdown(ai_reply)
                            st.session_state.expense_chat_history.append({"role": "assistant", "content": ai_reply})
                            
                            st.session_state["ai_parsed_data"] = {
                                "loai": loai,
                                "so_tien": so_tien,
                                "danh_muc": danh_muc,
                                "ngay": today_str,
                                "mo_ta": mo_ta,
                                "raw_prompt": user_exp_input
                            }
                            st.rerun()
                        else:
                            err_msg = "❌ Chưa nhận diện được số tiền hoặc loại giao dịch hợp lý trong câu. Bạn vui lòng thử gõ lại rõ hơn nhé (VD: 'Ăn phở 35k', 'Chiều tiêu 5 củ')!"
                            st.markdown(err_msg)
                            st.session_state.expense_chat_history.append({"role": "assistant", "content": err_msg})

        if "ai_parsed_data" in st.session_state:
            parsed_info = st.session_state["ai_parsed_data"]
            st.markdown("---")
            st.info(f"💡 AI đang chờ bạn xác nhận khoản: **{parsed_info['loai']} - {parsed_info['so_tien']:,.0f} ₫ ({parsed_info['danh_muc']})**")
            
            c_act1, c_act2 = st.columns([1, 1])
            with c_act1:
                if st.button("💾 Xác Nhận Ghi Khoản Này Vào Sổ", type="primary", key="confirm_exp_chat_save", use_container_width=True):
                    add_transaction(
                        parsed_info["loai"],
                        parsed_info["so_tien"],
                        parsed_info["danh_muc"],
                        parsed_info["ngay"],
                        parsed_info["mo_ta"]
                    )
                    del st.session_state["ai_parsed_data"]
            with c_act2:
                if st.button("✏️ Hủy Khoản Này", type="secondary", key="cancel_exp_chat_save", use_container_width=True):
                    del st.session_state["ai_parsed_data"]
                    st.rerun()

        st.markdown("---")
        st.subheader("📝 Nhập Giao Dịch Thủ Công")
        
        with st.form("manual_add_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                loai_input = st.radio("Loại giao dịch", ["Chi", "Thu"], horizontal=True, key="f_loai")
                so_tien_input = st.number_input("Số tiền (VND)", min_value=0.0, step=10000.0, format="%.0f", key="f_sotien")
                danh_muc_input = st.selectbox("Danh mục chi/thu", STUDENT_CATEGORIES, key="f_danhmuc")

            with f_col2:
                ngay_input = st.date_input("Ngày giao dịch", datetime.date.today(), key="f_ngay")
                ghi_chu_input = st.text_input("Ghi chú / Mô tả", placeholder="Ví dụ: Cơm trưa, đóng học phí, xăng xe...", key="f_ghichu")

            submit_btn = st.form_submit_button("💾 Lưu Vào Sổ Thu Chi", type="primary")
            if submit_btn:
                if so_tien_input <= 0:
                    st.error("Số tiền phải lớn hơn 0!")
                else:
                    add_transaction(loai_input, so_tien_input, danh_muc_input, ngay_input.strftime("%Y-%m-%d"), ghi_chu_input)

    with tab3:
        st.subheader("📜 Lịch Sử Chi Tiêu")
        
        f1, f2, f3 = st.columns(3)
        with f1:
            kw_filter = st.text_input("🔍 Tìm kiếm tên khoản chi/thu", key="kw_search")
        with f2:
            cat_filter = st.selectbox("🎯 Lọc theo danh mục", ["Tất cả"] + STUDENT_CATEGORIES, key="cat_select")
        with f3:
            if not df_all.empty and "ngay" in df_all.columns:
                months = sorted(list(set(pd.to_datetime(df_all["ngay"]).dt.strftime("%Y-%m"))), reverse=True)
                avail_months = ["Tất cả"] + months
            else:
                avail_months = ["Tất cả"]
            month_filter = st.selectbox("📅 Lọc theo tháng", avail_months, key="month_select")

        df_filtered = df_all.copy() if not df_all.empty else pd.DataFrame()
        if not df_filtered.empty:
            if kw_filter:
                kw = kw_filter.lower()
                df_filtered = df_filtered[
                    df_filtered["ghi_chu"].fillna("").astype(str).str.lower().str.contains(kw) |
                    df_filtered["danh_muc"].astype(str).str.lower().str.contains(kw)
                ]
            if cat_filter != "Tất cả":
                df_filtered = df_filtered[df_filtered["danh_muc"] == cat_filter]
            if month_filter != "Tất cả":
                df_filtered = df_filtered[pd.to_datetime(df_filtered["ngay"]).dt.strftime("%Y-%m") == month_filter]

        if not df_filtered.empty:
            st.dataframe(
                df_filtered.rename(columns={
                    "id": "ID", "loai": "Loại", "so_tien": "Số Tiền (VND)",
                    "danh_muc": "Danh Mục", "ngay": "Ngày", "ghi_chu": "Ghi Chú"
                }),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("#### ⚙️ Chỉnh Sửa Hoặc Xóa Khoản Thu Chi")
            edit_col1, edit_col2 = st.columns([1, 1])
            
            with edit_col1:
                st.markdown("##### ✏️ Chỉnh Sửa Giao Dịch")
                selected_edit_id = st.selectbox("Chọn ID để sửa", df_filtered["id"].tolist(), key="sb_edit_id")
                selected_row = df_filtered[df_filtered["id"] == selected_edit_id].iloc[0]
                
                with st.form("edit_transaction_form"):
                    e_loai = st.radio("Loại", ["Chi", "Thu"], index=0 if selected_row["loai"] == "Chi" else 1, horizontal=True)
                    e_amt = st.number_input("Số tiền (VND)", value=float(selected_row["so_tien"]), step=10000.0, format="%.0f")
                    e_cat = st.selectbox(
                        "Danh mục", 
                        STUDENT_CATEGORIES, 
                        index=STUDENT_CATEGORIES.index(selected_row["danh_muc"]) if selected_row["danh_muc"] in STUDENT_CATEGORIES else 0
                    )
                    e_date = st.date_input("Ngày", datetime.datetime.strptime(selected_row["ngay"], "%Y-%m-%d").date())
                    e_note = st.text_input("Ghi chú", value=str(selected_row["ghi_chu"] if selected_row["ghi_chu"] else ""))
                    
                    if st.form_submit_button("💾 Lưu Thay Đổi", type="primary"):
                        update_transaction(selected_edit_id, e_loai, e_amt, e_cat, e_date.strftime("%Y-%m-%d"), e_note)

            with edit_col2:
                st.markdown("##### 🗑️ Xóa Giao Dịch")
                selected_del_id = st.selectbox("Chọn ID để xóa", df_filtered["id"].tolist(), key="sb_del_id")
                
                del_row = df_filtered[df_filtered["id"] == selected_del_id].iloc[0]
                st.warning(f"⚠️ Bạn sắp xóa: **{del_row['loai']}** — {float(del_row['so_tien']):,.0f} ₫ ({del_row['danh_muc']}) — {del_row['ghi_chu']}")
                
                confirm_del = st.checkbox("Tôi xác nhận muốn xóa giao dịch này", key="confirm_del_checkbox")
                if st.button("🗑️ Xác Nhận Xóa", type="secondary", key="del_confirm_btn", disabled=not confirm_del):
                    delete_transaction(selected_del_id)
        else:
            st.info("Chưa tìm thấy dòng thu chi nào phù hợp.")

        st.markdown("---")
        st.subheader("📂 Xuất / Nhập Dữ Liệu")
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            st.markdown("##### 📥 Xuất File Báo Cáo")
            if not df_filtered.empty:
                csv_data = df_filtered.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Tải Báo Cáo CSV",
                    data=csv_data,
                    file_name=f"thu_chi_sinh_vien_{datetime.date.today()}.csv",
                    mime="text/csv"
                )
                
                output_excel = io.BytesIO()
                with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                    df_filtered.to_excel(writer, index=False, sheet_name='ThuChiSinhVien')
                st.download_button(
                    label="📊 Tải Báo Cáo Excel (.xlsx)",
                    data=output_excel.getvalue(),
                    file_name=f"thu_chi_sinh_vien_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.caption("Chưa có dữ liệu để xuất file.")

        with exp_col2:
            st.markdown("##### 📤 Nhập Dữ Liệu Từ File CSV")
            uploaded_file = st.file_uploader("Tải file CSV (gồm các cột: loai, so_tien, danh_muc, ngay, ghi_chu)", type=["csv"], key="csv_import")
            if uploaded_file is not None:
                try:
                    imp_df = pd.read_csv(uploaded_file)
                    if st.button("🚀 XÁC NHẬN NHẬP DỮ LIỆU", type="primary", key="csv_import_confirm"):
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        count = 0
                        for _, row in imp_df.iterrows():
                            cursor.execute(
                                "INSERT INTO giao_dich (loai, so_tien, danh_muc, ngay, ghi_chu) VALUES (?, ?, ?, ?, ?)",
                                (str(row["loai"]), float(row["so_tien"]), str(row["danh_muc"]), str(row["ngay"]), str(row.get("ghi_chu", "")))
                            )
                            count += 1
                        conn.commit()
                        conn.close()
                        st.session_state["toast_msg"] = f"📥 Đã nhập thành công {count} khoản thu chi!"
                        load_data()
                        st.rerun()
                except Exception as ex:
                    st.error(f"Lỗi đọc file CSV: {ex}")

    with tab4:
        st.subheader("🧠 Trợ Lý AI Tư Vấn Tiết Kiệm Cho Sinh Viên")
        st.caption("Google Gemini AI sẽ phân tích thói quen chi tiêu của bạn và đưa ra lời khuyên thực tế để tiết kiệm hiệu quả.")

        if st.button("📊 Phân Tích & Đưa Lời Khuyên Mới Nhất", type="primary", key="advice_btn"):
            if check_ai_key():
                with st.spinner("Trợ lý Gemini đang phân tích tình trạng tài chính của bạn..."):
                    advice = generate_savings_advice(df_all)
                    st.markdown(advice)

    render_floating_cskh_widget(df_all, summary, budget_limits)

    st.markdown("""
        <div class="app-footer">
            Powered by <strong>Google Gemini AI</strong> & <strong>Streamlit</strong> | Made with ❤️ for Students 🎓
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
