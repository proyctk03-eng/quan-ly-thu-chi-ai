# ------------------------------------------------------------------------------
# STREAMLIT FRONTEND — CALLS FASTAPI BACKEND VIA HTTP REST API
# ------------------------------------------------------------------------------
import datetime
import io
import json
import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from typing import TypedDict

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Config page
st.set_page_config(
    page_title="Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# ------------------------------------------------------------------------------
# API CLIENT HELPERS
# ------------------------------------------------------------------------------
def api_get(endpoint: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE_URL}{endpoint}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"❌ Lỗi kết nối Backend API ({endpoint}): {e}")
        return None

def api_post(endpoint: str, json_data: dict = None):
    try:
        r = requests.post(f"{API_BASE_URL}{endpoint}", json=json_data, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"❌ Lỗi gửi request Backend API ({endpoint}): {e}")
        return None

def api_put(endpoint: str, json_data: dict = None):
    try:
        r = requests.put(f"{API_BASE_URL}{endpoint}", json=json_data, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"❌ Lỗi cập nhật Backend API ({endpoint}): {e}")
        return None

def api_delete(endpoint: str):
    try:
        r = requests.delete(f"{API_BASE_URL}{endpoint}", timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        st.error(f"❌ Lỗi xóa qua Backend API ({endpoint}): {e}")
        return False

# Data Loader
def load_data():
    txs = api_get("/api/transactions")
    if txs is not None:
        st.session_state["df_transactions"] = pd.DataFrame(txs)
    else:
        st.session_state["df_transactions"] = pd.DataFrame()

    summary = api_get("/api/analytics/summary")
    if summary:
        st.session_state["summary"] = summary
    else:
        st.session_state["summary"] = {"tong_thu": 0.0, "tong_chi": 0.0, "so_du": 0.0}

    limits = api_get("/api/budgets")
    if limits:
        st.session_state["budget_limits"] = limits
    else:
        st.session_state["budget_limits"] = {}

if "df_transactions" not in st.session_state:
    load_data()

# CRUD helpers
def add_transaction(loai, so_tien, danh_muc, ngay, ghi_chu):
    payload = {"loai": loai, "so_tien": float(so_tien), "danh_muc": danh_muc, "ngay": ngay, "ghi_chu": ghi_chu}
    res = api_post("/api/transactions", payload)
    if res:
        st.session_state["toast_msg"] = f"✅ Đã thêm giao dịch: {loai} {so_tien:,.0f} ₫ ({danh_muc})"
        load_data()
        st.rerun()

def update_transaction(id_gd, loai, so_tien, danh_muc, ngay, ghi_chu):
    payload = {"loai": loai, "so_tien": float(so_tien), "danh_muc": danh_muc, "ngay": ngay, "ghi_chu": ghi_chu}
    res = api_put(f"/api/transactions/{id_gd}", payload)
    if res:
        st.session_state["toast_msg"] = f"✏️ Đã cập nhật thành công giao dịch ID #{id_gd}!"
        load_data()
        st.rerun()

def delete_transaction(id_gd):
    ok = api_delete(f"/api/transactions/{id_gd}")
    if ok:
        st.session_state["toast_msg"] = f"🗑️ Đã xóa thành công giao dịch ID #{id_gd}!"
        load_data()
        st.rerun()

def set_budget_limit(danh_muc, limit_val):
    payload = {"danh_muc": danh_muc, "so_tien_limit": float(limit_val)}
    res = api_post("/api/budgets", payload)
    if res:
        st.session_state["toast_msg"] = f"🎯 Đã đặt hạn mức '{danh_muc}': {limit_val:,.0f} ₫"
        load_data()
        st.rerun()

# ------------------------------------------------------------------------------
# PLOTLY CHARTS
# ------------------------------------------------------------------------------
def draw_pie_chart(df_all):
    if df_all.empty:
        st.info("Chưa có dữ liệu chi tiêu để vẽ biểu đồ phân phối.")
        return
    df_chi = df_all[df_all["loai"] == "Chi"]
    if not df_chi.empty:
        cat_summary = df_chi.groupby("danh_muc")["so_tien"].sum().reset_index()
        STUDENT_PALETTE = ['#0EA5E9', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#64748B']
        fig_pie = px.pie(cat_summary, values="so_tien", names="danh_muc", hole=0.45, color_discrete_sequence=STUDENT_PALETTE)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(width=2)))
        fig_pie.update_layout(margin=dict(t=30, b=30, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit")
    else:
        st.info("Chưa có dữ liệu chi tiêu để vẽ biểu đồ phân phối.")

def draw_bar_chart(df_all):
    if df_all.empty:
        return
    df_all_copy = df_all.copy()
    df_all_copy["thang"] = pd.to_datetime(df_all_copy["ngay"]).dt.strftime("%Y-%m")
    monthly_summary = df_all_copy.groupby(["thang", "loai"])["so_tien"].sum().reset_index()
    fig_bar = px.bar(monthly_summary, x="thang", y="so_tien", color="loai", barmode="group", color_discrete_map={"Thu": "#10B981", "Chi": "#EF4444"}, labels={"so_tien": "Số tiền (VND)", "thang": "Tháng"})
    fig_bar.update_layout(margin=dict(t=30, b=30, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit")

def draw_line_chart(df_all):
    if df_all.empty:
        st.info("Chưa có dữ liệu chi tiêu để vẽ biểu đồ xu hướng.")
        return
    df_chi = df_all[df_all["loai"] == "Chi"].copy()
    if df_chi.empty:
        st.info("Chưa có dữ liệu chi tiêu tháng này.")
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
    fig_line = px.line(daily, x="Ngày", y="Tích lũy", markers=True, labels={"Tích lũy": "Chi tiêu tích lũy (VND)", "Ngày": ""}, color_discrete_sequence=["#0EA5E9"])
    fig_line.add_bar(x=daily["Ngày"], y=daily["Tổng chi"], name="Chi tiêu/ngày", marker_color="rgba(239, 68, 68, 0.4)")
    fig_line.update_layout(margin=dict(t=30, b=30, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True, theme="streamlit")

# ------------------------------------------------------------------------------
# INJECT CUSTOM STYLE
# ------------------------------------------------------------------------------
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; }
        .stApp { background-color: var(--background-color) !important; color: var(--text-color) !important; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
        .stTabs, div[data-testid="stMetric"], .stForm { animation: fadeInUp 0.5s ease-out both; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, color-mix(in srgb, var(--secondary-background-color) 85%, transparent) 0%, var(--secondary-background-color) 100%) !important; backdrop-filter: blur(12px) !important; border-right: 1px solid rgba(128, 128, 128, 0.12) !important; }
        .student-header { font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 50%, #10B981 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; margin-bottom: 0.2rem; animation: shimmer 4s linear infinite; }
        div[data-testid="stMetric"] { background: var(--secondary-background-color) !important; border: 1px solid rgba(128, 128, 128, 0.12) !important; border-radius: 16px !important; padding: 18px 22px !important; transition: all 0.25s ease !important; }
        div[data-testid="stMetric"]:hover { transform: translateY(-4px) !important; box-shadow: 0 8px 25px rgba(14, 165, 233, 0.15) !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: var(--secondary-background-color); padding: 6px; border-radius: 14px; }
        .stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 10px 18px; font-weight: 600; }
        .health-card { padding: 14px 18px; border-radius: 14px; border: 1px solid rgba(128, 128, 128, 0.12); background: var(--secondary-background-color); margin-bottom: 12px; }
        .health-score { font-size: 2rem; font-weight: 800; text-align: center; margin: 4px 0; }
        .health-label { font-size: 0.8rem; text-align: center; opacity: 0.7; }
        .app-footer { text-align: center; padding: 20px 0 10px 0; opacity: 0.5; font-size: 0.8rem; border-top: 1px solid rgba(128, 128, 128, 0.12); margin-top: 40px; }
        div[data-testid="stPopover"] { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 99999 !important; }
        div[data-testid="stPopover"] button { border-radius: 50% !important; width: 65px !important; height: 65px !important; background-color: #4C6EF5 !important; border: none !important; box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important; }
        div[data-testid="stPopoverBody"] { border-radius: 20px !important; padding: 16px !important; width: 380px !important; }
        </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# COMPONENTS
# ------------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/isometric/100/student-male.png", width=75)
        st.markdown("<h2 style='font-weight:800; font-size:1.35rem;'>🎓 Sổ Tay Sinh Viên</h2>", unsafe_allow_html=True)
        st.caption("Quản lý tài chính cá nhân thông minh & tiết kiệm")
        if st.button("🔄 Đồng bộ dữ liệu mới", use_container_width=True, type="secondary", key="sb_sync_btn"):
            load_data()
            st.session_state["toast_msg"] = "🔄 Đã cập nhật dữ liệu từ Backend API!"
            st.rerun()

        st.markdown("---")
        st.subheader("🎯 Đặt Hạn Mức Tiêu Tháng")
        selected_b_cat = st.selectbox("Chọn khoản chi", STUDENT_CATEGORIES[:6], key="sb_budget_cat")
        b_limit_val = st.number_input("Hạn mức tối đa (VND)", min_value=100000.0, step=100000.0, value=2000000.0, format="%.0f", key="sb_budget_val")
        if st.button("💾 Đặt Hạn Mức", type="primary", use_container_width=True, key="sb_save_limit_btn"):
            set_budget_limit(selected_b_cat, b_limit_val)

        st.markdown("---")
        st.subheader("💚 Sức Khỏe Tài Chính")
        sb_summary = st.session_state.get("summary", {"tong_thu": 0, "tong_chi": 0, "so_du": 0})
        sb_thu = sb_summary.get("tong_thu", 0)
        sb_chi = sb_summary.get("tong_chi", 0)
        saving_rate = ((sb_thu - sb_chi) / sb_thu * 100) if sb_thu > 0 else 0
        score_color = "#10B981" if saving_rate >= 20 else ("#F59E0B" if saving_rate >= 10 else ("#EF4444" if saving_rate >= 0 else "#DC2626"))
        score_label = "Tuyệt vời! 🌟" if saving_rate >= 20 else ("Tạm ổn 👍" if saving_rate >= 10 else ("Cần cải thiện ⚠️" if saving_rate >= 0 else "Cháy túi! 🔥"))

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
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "👋 Chào bạn! Mình là **Trợ Lý CSKH AI 🎓**. Bạn cần mình hỗ trợ điều gì không?"}]
    with st.container():
        with st.popover("💬", use_container_width=False):
            st.markdown("### 💬 Trợ Lý CSKH & Điều Hành AI 🎓")
            if st.button("🗑️ Xóa Lịch Sử CSKH", key="clear_cskh_pop_btn", type="secondary", use_container_width=True):
                st.session_state.messages = [{"role": "assistant", "content": "👋 Chào bạn! Mình là **Trợ Lý CSKH AI 🎓**."}]
                st.rerun()
            chat_container = st.container(height=300)
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            pop_user_input = st.chat_input("Nhập yêu cầu CSKH...", key="pop_cskh_chat_input")
            if pop_user_input:
                st.session_state.messages.append({"role": "user", "content": pop_user_input})
                with st.spinner("Trợ lý CSKH AI đang thực thi..."):
                    res = api_post("/api/ai/agent", {"query": pop_user_input, "summary": summary, "budget_limits": budget_limits})
                    if res and res.get("success"):
                        agent_res = res.get("data", {})
                        action = agent_res.get("action", "CHAT")
                        reply_text = agent_res.get("reply", "Dạ em đã ghi nhận.")
                        if action == "ADD_TRANSACTION":
                            add_transaction(agent_res.get("loai", "Chi"), float(agent_res.get("so_tien", 0)), agent_res.get("danh_muc", "Khác"), datetime.date.today().strftime("%Y-%m-%d"), agent_res.get("ghi_chu", pop_user_input))
                        elif action == "DELETE_TRANSACTION":
                            delete_transaction(int(agent_res.get("id", 0)))
                        elif action == "SET_BUDGET":
                            set_budget_limit(agent_res.get("danh_muc", "Khác"), float(agent_res.get("limit_val", 0)))
                        st.session_state.messages.append({"role": "assistant", "content": reply_text})
                        st.rerun()

def render_header():
    header_col1, header_col2 = st.columns([0.8, 0.2])
    with header_col1:
        st.markdown('<div class="student-header">🎓 QUẢN LÝ CHI TIÊU SINH VIÊN AI</div>', unsafe_allow_html=True)
        st.caption("Sổ tay quản lý ví sinh viên thông minh 🍜 (FastAPI Backend Architecture)")
    with header_col2:
        if st.button("🔄 Làm mới dữ liệu", key="header_refresh", type="secondary"):
            load_data()
            st.session_state["toast_msg"] = "🔄 Dữ liệu ví sinh viên đã được đồng bộ mới nhất!"
            st.rerun()
    if "toast_msg" in st.session_state and st.session_state["toast_msg"]:
        st.toast(st.session_state.pop("toast_msg"), icon="🎒")

# ------------------------------------------------------------------------------
# MAIN ROUTING
# ------------------------------------------------------------------------------
def main():
    inject_custom_css()
    render_sidebar()
    render_header()

    df_all = st.session_state.get("df_transactions", pd.DataFrame())
    summary = st.session_state.get("summary", {"tong_thu": 0.0, "tong_chi": 0.0, "so_du": 0.0})
    budget_limits = st.session_state.get("budget_limits", {})

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Thống Kê", "➕ Thêm Chi Tiêu", "📜 Lịch Sử", "🧠 Gợi Ý Tiết Kiệm", "🤖 Trợ Lý Gemini"])

    with tab1:
        tong_thu = summary.get("tong_thu", 0.0)
        tong_chi = summary.get("tong_chi", 0.0)
        so_du = summary.get("so_du", 0.0)
        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Tổng Tiền Nhận (Thu)", f"{tong_thu:,.0f} ₫")
        c2.metric("🔴 Tổng Tiền Tiêu (Chi)", f"{tong_chi:,.0f} ₫")
        c3.metric("💰 Số Dư Ví Sinh Viên", f"{so_du:,.0f} ₫", delta=f"{so_du:,.0f} ₫" if so_du >= 0 else "Cảnh báo hết tiền!", delta_color="normal" if so_du >= 0 else "inverse")

        # Month comparison from Backend API
        cmp_res = api_get("/api/analytics/monthly-comparison")
        if cmp_res:
            cmp_c1, cmp_c2 = st.columns(2)
            cmp_c1.metric(f"🔴 Chi Tiêu Tháng {cmp_res['current_month']}", f"{cmp_res['chi_this']:,.0f} ₫", delta=f"{cmp_res['chi_delta']:+,.0f} ₫ ({cmp_res['chi_delta_pct']})", delta_color="inverse")
            cmp_c2.metric(f"🟢 Thu Nhập Tháng {cmp_res['current_month']}", f"{cmp_res['thu_this']:,.0f} ₫", delta=f"{cmp_res['thu_delta']:+,.0f} ₫ ({cmp_res['thu_delta_pct']})", delta_color="normal")

        st.markdown("---")
        st.subheader("🎯 Hạn Mức Chi Tiêu Cho Sinh Viên Tháng Này")
        if not df_all.empty and budget_limits:
            df_chi = df_all[df_all["loai"] == "Chi"]
            spent_by_cat = df_chi.groupby("danh_muc")["so_tien"].sum().to_dict() if not df_chi.empty else {}
            b_cols = st.columns(min(len(budget_limits), 4))
            col_idx = 0
            for cat, limit_amt in budget_limits.items():
                spent = spent_by_cat.get(cat, 0.0)
                pct = min(spent / limit_amt, 1.0) if limit_amt > 0 else 0.0
                with b_cols[col_idx % len(b_cols)]:
                    st.markdown(f"**{cat}**")
                    st.caption(f"Đã tiêu: {spent:,.0f} / {limit_amt:,.0f} ₫ ({pct*100:.1f}%)")
                    st.progress(pct)
                    col_idx += 1

        st.markdown("---")
        if not df_all.empty:
            cc1, cc2 = st.columns(2)
            with cc1:
                st.subheader("🥧 Các Khoản Chi Chiếm Nhiều Tiền Nhất")
                draw_pie_chart(df_all)
            with cc2:
                st.subheader("📊 Thu vs Chi Theo Tháng")
                draw_bar_chart(df_all)
            st.markdown("---")
            st.subheader("📈 Xu Hướng Chi Tiêu Tháng Này (Theo Ngày)")
            draw_line_chart(df_all)

    with tab2:
        st.subheader("🤖 Trợ Lý AI Nhập Chi Tiêu & Cố Vấn Tài Chính")
        if "expense_chat_history" not in st.session_state:
            st.session_state.expense_chat_history = [{"role": "assistant", "content": "Chào bạn! Gõ cho mình biết khoản thu/chi của bạn nhé!"}]
        for msg in st.session_state.expense_chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        user_exp_input = st.chat_input("Gõ câu chi tiêu hoặc thu nhập của bạn...", key="tab2_chat_input")
        if user_exp_input:
            st.session_state.expense_chat_history.append({"role": "user", "content": user_exp_input})
            with st.spinner("Gemini đang bóc tách qua Backend API..."):
                res = api_post("/api/ai/parse-expense", {"prompt": user_exp_input, "summary": summary, "budget_limits": budget_limits})
                if res and res.get("success") and res.get("data"):
                    result = res["data"]
                    loai = "Thu" if str(result.get("type", "")).lower() == "thu" else "Chi"
                    so_tien = float(result.get("amount", 0))
                    category_mapping = {"Ăn uống & Cafe": "Ăn uống & Cafe", "Di chuyển": "Di chuyển & Xăng xe", "Giải trí": "Giải trí & Bè bạn", "Mua sắm": "Mua sắm cá nhân", "Hóa đơn": "Tiền nhà & Tiện ích", "Khác": "Khác"}
                    danh_muc = category_mapping.get(str(result.get("category", "Khác")), "Khác")
                    mo_ta = str(result.get("description", user_exp_input))
                    ai_reply = f"📌 **Bóc tách**: {loai} - **{so_tien:,.0f} ₫** ({danh_muc})\n💡 **Gợi ý**: {result.get('smart_advice','')}"
                    st.session_state.expense_chat_history.append({"role": "assistant", "content": ai_reply})
                    st.session_state["ai_parsed_data"] = {"loai": loai, "so_tien": so_tien, "danh_muc": danh_muc, "ngay": datetime.date.today().strftime("%Y-%m-%d"), "mo_ta": mo_ta}
                    st.rerun()

        if "ai_parsed_data" in st.session_state:
            parsed_info = st.session_state["ai_parsed_data"]
            st.info(f"💡 Xác nhận: **{parsed_info['loai']} - {parsed_info['so_tien']:,.0f} ₫ ({parsed_info['danh_muc']})**")
            if st.button("💾 Xác Nhận Ghi Khoản Này", type="primary"):
                add_transaction(parsed_info["loai"], parsed_info["so_tien"], parsed_info["danh_muc"], parsed_info["ngay"], parsed_info["mo_ta"])
                del st.session_state["ai_parsed_data"]

        st.markdown("---")
        st.subheader("📝 Nhập Giao Dịch Thủ Công")
        with st.form("manual_add_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                loai_input = st.radio("Loại giao dịch", ["Chi", "Thu"], horizontal=True)
                so_tien_input = st.number_input("Số tiền (VND)", min_value=0.0, step=10000.0, format="%.0f")
                danh_muc_input = st.selectbox("Danh mục", STUDENT_CATEGORIES)
            with f_col2:
                ngay_input = st.date_input("Ngày", datetime.date.today())
                ghi_chu_input = st.text_input("Ghi chú")
            if st.form_submit_button("💾 Lưu Vào Sổ"):
                if so_tien_input > 0:
                    add_transaction(loai_input, so_tien_input, danh_muc_input, ngay_input.strftime("%Y-%m-%d"), ghi_chu_input)

    with tab3:
        st.subheader("📜 Lịch Sử Chi Tiêu")
        if not df_all.empty:
            st.dataframe(df_all.rename(columns={"id": "ID", "loai": "Loại", "so_tien": "Số Tiền (VND)", "danh_muc": "Danh Mục", "ngay": "Ngày", "ghi_chu": "Ghi Chú"}), use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("🧠 Trợ Lý AI Tư Vấn Tiết Kiệm Cho Sinh Viên")
        if st.button("📊 Phân Tích & Đưa Lời Khuyên Mới Nhất", type="primary"):
            csv_str = df_all.to_csv(index=False) if not df_all.empty else ""
            res = api_post("/api/ai/savings-advice", {"transactions_csv": csv_str})
            if res and res.get("success"):
                st.markdown(res.get("data", ""))

    with tab5:
        st.subheader("💬 Hỏi Đáp Cùng Trợ Lý Sinh Viên AI Gemini")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [{"role": "assistant", "content": "Chào bạn! Mình là Trợ lý AI Sinh Viên Gemini 🎓."}]
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        user_query = st.chat_input("Nhập câu hỏi...")
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            res = api_post("/api/ai/chat", {"query": user_query, "chat_history": st.session_state.chat_history})
            if res and res.get("success"):
                ans = res.get("data")
                st.session_state.chat_history.append({"role": "assistant", "content": ans})
                st.rerun()

    render_floating_cskh_widget(df_all, summary, budget_limits)
    st.markdown('<div class="app-footer">Powered by <strong>FastAPI</strong> & <strong>Streamlit</strong> 🎓</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
