"""Gemini AI API endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, status

from backend.models.schemas import (
    AIAgentRequest,
    AIChatRequest,
    AIParseRequest,
    AIResponse,
    AISavingsAdviceRequest,
)
from backend.services import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI Services"])


@router.post("/parse-expense", response_model=AIResponse)
def parse_expense(payload: AIParseRequest) -> dict[str, Any]:
    """Parse natural language expense using Gemini."""
    try:
        data = ai_service.analyze_natural_language_expense(
            prompt_input=payload.prompt,
            summary_info=payload.summary,
            budget_limits=payload.budget_limits,
        )
        return {"success": True, "data": data}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


@router.post("/savings-advice", response_model=AIResponse)
def get_savings_advice(payload: AISavingsAdviceRequest) -> dict[str, Any]:
    """Get AI savings advice."""
    try:
        advice = ai_service.generate_savings_advice(payload.transactions_csv)
        return {"success": True, "data": advice}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


@router.post("/chat", response_model=AIResponse)
def chat_ai(payload: AIChatRequest) -> dict[str, Any]:
    """Chat with Gemini Assistant."""
    try:
        reply = ai_service.chat_with_gemini(
            chat_history=payload.chat_history,
            user_query=payload.query,
        )
        return {"success": True, "data": reply}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


@router.post("/agent", response_model=AIResponse)
def agent_cskh(payload: AIAgentRequest) -> dict[str, Any]:
    """CSKH Agent intent recognition."""
    try:
        action = ai_service.chat_with_gemini_agent(
            user_query=payload.query,
            summary=payload.summary,
            budget_limits=payload.budget_limits,
        )
        return {"success": True, "data": action}
    except Exception as exc:
        return {"success": False, "error": str(exc)}
