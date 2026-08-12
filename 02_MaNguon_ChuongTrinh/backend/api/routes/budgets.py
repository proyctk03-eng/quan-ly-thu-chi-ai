"""Budgets API endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, status

from backend.models.schemas import BudgetLimitResponse, BudgetLimitSet
from backend.services import budget_service

router = APIRouter(prefix="/api/budgets", tags=["Budgets"])


@router.get("", response_model=dict[str, float])
def get_budgets() -> dict[str, float]:
    """Get dictionary of category budget limits."""
    return budget_service.get_budget_limits()


@router.get("/list", response_model=list[BudgetLimitResponse])
def get_budgets_list() -> list[dict[str, Any]]:
    """Get list of budget limits."""
    return budget_service.get_all_limits_list()


@router.post("", status_code=status.HTTP_200_OK)
def set_budget(payload: BudgetLimitSet) -> dict[str, str]:
    """Set or update budget limit for a category."""
    budget_service.set_budget_limit(payload.danh_muc, payload.so_tien_limit)
    return {"status": "success", "message": f"Set limit for {payload.danh_muc}"}
