"""Gemini AI service — proxy-aware, geo-block-safe, no Streamlit."""

from __future__ import annotations

import json
from typing import Any

import google.generativeai as genai

from backend.core.config import (
    GEO_BLOCK_MSG,
    GEMINI_API_KEY,
    GEMINI_MODEL_NAME,
    inject_proxy,
    is_geo_blocked_error,
)


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------
def init_gemini() -> bool:
    """Configure the ``genai`` library; return *True* on success."""
    if not GEMINI_API_KEY:
        return False
    try:
        inject_proxy()
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception as exc:
        if is_geo_blocked_error(exc):
            raise RuntimeError(GEO_BLOCK_MSG) from exc
        raise


# ---------------------------------------------------------------------------
# 1. Parse natural-language expense
# ---------------------------------------------------------------------------
def analyze_natural_language_expense(
    prompt_input: str,
    summary_info: dict[str, Any] | None = None,
    budget_limits: dict[str, float] | None = None,
) -> dict[str, Any] | None:
    """Use Gemini to extract a transaction from natural language."""
    if not init_gemini():
        return None

    ctx_thu = (summary_info or {}).get("tong_thu", 0)
    ctx_chi = (summary_info or {}).get("tong_chi", 0)
    ctx_so_du = (summary_info or {}).get("so_du", 0)
    limits_str = (
        json.dumps(budget_limits, ensure_ascii=False)
        if budget_limits
        else "Chưa đặt"
    )

    system_prompt = (
        "[Instructions]\n"
        "Bạn là Chuyên gia Cố vấn Quản lý Tài chính Sinh Viên AI. "
        "Hãy thực hiện bóc tách giao dịch từ câu nói người dùng, "
        "phân tích mức độ rủi ro, tác động ví, gợi ý định mức sinh viên "
        "và tư tưởng/hệ lụy tài chính.\n\n"
        "[Context]\n"
        "- Người dùng là sinh viên đại học quản lý ví cá nhân.\n"
        f"- Bối cảnh tài chính tháng hiện tại: Thu nhập {ctx_thu:,.0f} VNĐ, "
        f"Đã chi {ctx_chi:,.0f} VNĐ, Số dư ví {ctx_so_du:,.0f} VNĐ.\n"
        f"- Hạn mức danh mục: {limits_str}.\n\n"
        "[Input Data / Constraints]\n"
        "1. amount: Số nguyên VNĐ (> 0). Quy đổi từ lóng "
        "('199k' -> 199000, '5 củ' -> 5000000). "
        "Nếu có nhiều khoản chi/thu trong câu, cộng tổng tất cả lại.\n"
        "2. type: 'chi' hoặc 'thu'.\n"
        "3. category: Chọn đúng 1 trong các danh mục sinh viên: "
        "'Ăn uống & Cafe', 'Di chuyển', 'Giải trí', "
        "'Mua sắm', 'Hóa đơn', 'Khác'.\n"
        "4. warning_level: 'SAFE', 'WARNING', 'CRITICAL'.\n"
        "5. Đầy đủ các trường: type, amount, category, description, "
        "warning_level, financial_impact, smart_advice, consequences.\n\n"
        "[Output Format]\n"
        "JSON Object duy nhất chuẩn định dạng 8 trường trên."
    )

    generation_config = genai.types.GenerationConfig(
        temperature=0.2,
        response_mime_type="application/json",
    )

    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            system_instruction=system_prompt,
            generation_config=generation_config,
        )
        response = model.generate_content(prompt_input)
        parsed = json.loads(response.text)

        if isinstance(parsed, list):
            if parsed and isinstance(parsed[0], dict):
                first = parsed[0]
                first["amount"] = sum(
                    float(i.get("amount", 0))
                    for i in parsed
                    if isinstance(i, dict)
                )
                return first
            return None
        if isinstance(parsed, dict):
            return parsed
        return None
    except Exception as exc:
        if is_geo_blocked_error(exc):
            raise RuntimeError(GEO_BLOCK_MSG) from exc
        raise


# ---------------------------------------------------------------------------
# 2. Generate savings advice
# ---------------------------------------------------------------------------
def generate_savings_advice(transactions_csv: str) -> str:
    """Analyse CSV data and return markdown advice."""
    if not init_gemini():
        return "Chưa cấu hình API Key thích hợp."

    system_prompt = (
        "[Instructions]\n"
        "Bạn là Chuyên gia Cố vấn Quản lý Tài chính Sinh Viên "
        "& Giải Toán AI. Phân tích lịch sử chi tiêu từ dữ liệu CSV "
        "và đưa ra lời khuyên tiết kiệm súc tích, mạch lạc.\n\n"
        "[Context]\n"
        "- Hệ thống hỗ trợ quản lý ví sinh viên.\n"
        "- Phạm vi cho phép: Quản lý tài chính & tiết kiệm; "
        "Toán học & tư duy logic.\n"
        "- Phạm vi từ chối: Mọi chủ đề khác.\n\n"
        "[Output Format]\n"
        "Markdown trình bày đẹp mắt với các gạch đầu dòng "
        "phân tích & lời khuyên hành động."
    )

    generation_config = genai.types.GenerationConfig(temperature=0.3)

    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            system_instruction=system_prompt,
            generation_config=generation_config,
        )
        prompt = (
            "Dưới đây là danh sách thu chi cá nhân dạng CSV "
            "của một sinh viên:\n\n"
            f"{transactions_csv}\n\n"
            "Hãy phân tích và đưa ra lời khuyên tiết kiệm súc tích."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as exc:
        if is_geo_blocked_error(exc):
            return GEO_BLOCK_MSG
        return f"❌ Lỗi kết nối Gemini API: {exc}"


# ---------------------------------------------------------------------------
# 3. Chat with Gemini
# ---------------------------------------------------------------------------
def chat_with_gemini(
    chat_history: list[dict[str, str]],
    user_query: str,
    transactions_text: str = "",
) -> str | None:
    """Multi-turn chat; return the assistant reply or *None*."""
    if not init_gemini():
        return None

    ctx = transactions_text or "Chưa có dữ liệu giao dịch."
    system_instruction = (
        "[Instructions]\n"
        "Bạn là Trợ lý AI Sinh Viên Gemini chuyên biệt trong 2 lĩnh vực: "
        "QUẢN LÝ TÀI CHÍNH & GIẢI TOÁN HỌC.\n\n"
        "[Context]\n"
        "- Người dùng là sinh viên.\n"
        f"- Dữ liệu thu chi ví hiện tại:\n{ctx}\n\n"
        "[Constraints]\n"
        "- ALLOWLIST: Tài chính, toán học.\n"
        "- DENYLIST: Mọi chủ đề khác → từ chối.\n\n"
        "[Output Format]\n"
        "Markdown súc tích, mạch lạc."
    )

    generation_config = genai.types.GenerationConfig(temperature=0.3)

    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            system_instruction=system_instruction,
            generation_config=generation_config,
        )
        gemini_history = []
        for msg in chat_history[1:]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_query)
        return response.text
    except Exception as exc:
        if is_geo_blocked_error(exc):
            raise RuntimeError(GEO_BLOCK_MSG) from exc
        raise


# ---------------------------------------------------------------------------
# 4. Agentic CSKH
# ---------------------------------------------------------------------------
def chat_with_gemini_agent(
    user_query: str,
    transactions_text: str = "",
    summary: dict[str, Any] | None = None,
    budget_limits: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Intent-recognition agent: returns JSON action payload."""
    if not init_gemini():
        return {"action": "CHAT", "reply": "Chưa cấu hình Gemini API Key."}

    summary = summary or {}
    limits_str = (
        json.dumps(budget_limits, ensure_ascii=False)
        if budget_limits
        else "Chưa đặt"
    )

    system_instruction = (
        "[Instructions]\n"
        "Bạn là Trợ Lý CSKH & Cố Vấn Điều Hành AI của Sổ Tay Sinh Viên "
        "🎓. Bạn có quyền THỰC THI TRỰC TIẾP các hành động hệ thống.\n\n"
        "[Context]\n"
        f"- Thu {summary.get('tong_thu', 0):,.0f} ₫ | "
        f"Chi {summary.get('tong_chi', 0):,.0f} ₫ | "
        f"Số dư {summary.get('so_du', 0):,.0f} ₫\n"
        f"- Hạn mức: {limits_str}\n"
        f"- Giao dịch:\n{transactions_text}\n\n"
        "[Actions]\n"
        "1. ADD_TRANSACTION  2. DELETE_TRANSACTION  "
        "3. SET_BUDGET  4. CHAT\n\n"
        "[Output Format]\n"
        "JSON Object duy nhất chứa 'action' và các trường tương ứng."
    )

    generation_config = genai.types.GenerationConfig(
        temperature=0.2,
        response_mime_type="application/json",
    )

    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            system_instruction=system_instruction,
            generation_config=generation_config,
        )
        response = model.generate_content(user_query)
        parsed = json.loads(response.text)
        if isinstance(parsed, list) and parsed:
            parsed = parsed[0]
        return parsed
    except Exception as exc:
        if is_geo_blocked_error(exc):
            return {"action": "CHAT", "reply": GEO_BLOCK_MSG}
        return {
            "action": "CHAT",
            "reply": f"Rất tiếc có lỗi kết nối: {exc}",
        }
