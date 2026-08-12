"""Pydantic request / response schemas for the API."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Transaction schemas
# ---------------------------------------------------------------------------
class TransactionCreate(BaseModel):
    """Payload to create a new transaction."""

    loai: str = Field(..., description="'Chi' or 'Thu'")
    so_tien: float = Field(..., gt=0)
    danh_muc: str
    ngay: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    ghi_chu: Optional[str] = ""


class TransactionUpdate(BaseModel):
    """Payload to update an existing transaction."""

    loai: str
    so_tien: float = Field(..., gt=0)
    danh_muc: str
    ngay: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    ghi_chu: Optional[str] = ""


class TransactionResponse(BaseModel):
    """Single transaction returned from the API."""

    id: int
    loai: str
    so_tien: float
    danh_muc: str
    ngay: str
    ghi_chu: Optional[str] = ""


# ---------------------------------------------------------------------------
# Budget schemas
# ---------------------------------------------------------------------------
class BudgetLimitSet(BaseModel):
    """Payload to set a budget limit for a category."""

    danh_muc: str
    so_tien_limit: float = Field(..., gt=0)


class BudgetLimitResponse(BaseModel):
    """Single budget limit returned from the API."""

    danh_muc: str
    so_tien_limit: float


# ---------------------------------------------------------------------------
# Analytics schemas
# ---------------------------------------------------------------------------
class SummaryResponse(BaseModel):
    """Financial summary."""

    tong_thu: float = 0.0
    tong_chi: float = 0.0
    so_du: float = 0.0


class MonthlyComparisonResponse(BaseModel):
    """Month-over-month comparison."""

    current_month: str
    chi_this: float = 0.0
    chi_prev: float = 0.0
    chi_delta: float = 0.0
    chi_delta_pct: Optional[str] = "N/A"
    thu_this: float = 0.0
    thu_prev: float = 0.0
    thu_delta: float = 0.0
    thu_delta_pct: Optional[str] = "N/A"


# ---------------------------------------------------------------------------
# AI schemas
# ---------------------------------------------------------------------------
class AIParseRequest(BaseModel):
    """Natural-language expense to be parsed by Gemini."""

    prompt: str
    summary: Optional[dict[str, Any]] = None
    budget_limits: Optional[dict[str, float]] = None


class AIChatRequest(BaseModel):
    """Chat request with history."""

    query: str
    chat_history: list[dict[str, str]] = Field(default_factory=list)


class AIAgentRequest(BaseModel):
    """Agentic CSKH request."""

    query: str
    summary: Optional[dict[str, Any]] = None
    budget_limits: Optional[dict[str, float]] = None


class AISavingsAdviceRequest(BaseModel):
    """Request for savings advice based on transaction CSV."""

    transactions_csv: str


class AIResponse(BaseModel):
    """Generic AI response wrapper."""

    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
