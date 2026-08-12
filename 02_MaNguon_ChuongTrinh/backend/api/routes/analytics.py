"""Analytics API endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from backend.models.schemas import MonthlyComparisonResponse, SummaryResponse
from backend.services import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary", response_model=SummaryResponse)
def get_summary() -> dict[str, float]:
    """Get overall financial summary (tong_thu, tong_chi, so_du)."""
    return analytics_service.get_financial_summary()


@router.get("/monthly-comparison", response_model=MonthlyComparisonResponse)
def get_monthly_comparison() -> dict:
    """Get month-over-month financial comparison."""
    return analytics_service.get_monthly_comparison()
