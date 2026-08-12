"""Transactions API endpoints."""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, status

from backend.models.schemas import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from backend.services import transaction_service

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.get("", response_model=list[TransactionResponse])
def get_transactions(
    keyword: Optional[str] = Query(None, description="Search keyword"),
    category: Optional[str] = Query(None, description="Category filter"),
    month: Optional[str] = Query(None, description="YYYY-MM filter"),
) -> list[dict[str, Any]]:
    """List all transactions with optional filters."""
    return transaction_service.list_transactions(
        keyword=keyword, category=category, month=month
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int) -> dict[str, Any]:
    """Get single transaction by ID."""
    tx = transaction_service.get_transaction(transaction_id)
    if not tx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction #{transaction_id} not found",
        )
    return tx


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate) -> dict[str, Any]:
    """Create a new transaction."""
    new_id = transaction_service.add_transaction(
        loai=payload.loai,
        so_tien=payload.so_tien,
        danh_muc=payload.danh_muc,
        ngay=payload.ngay,
        ghi_chu=payload.ghi_chu or "",
    )
    tx = transaction_service.get_transaction(new_id)
    if not tx:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction",
        )
    return tx


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int, payload: TransactionUpdate
) -> dict[str, Any]:
    """Update existing transaction."""
    success = transaction_service.update_transaction(
        transaction_id=transaction_id,
        loai=payload.loai,
        so_tien=payload.so_tien,
        danh_muc=payload.danh_muc,
        ngay=payload.ngay,
        ghi_chu=payload.ghi_chu or "",
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction #{transaction_id} not found",
        )
    tx = transaction_service.get_transaction(transaction_id)
    return tx  # type: ignore[return-value]


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int) -> None:
    """Delete a transaction."""
    success = transaction_service.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction #{transaction_id} not found",
        )


@router.post("/import", status_code=status.HTTP_200_OK)
def bulk_import(rows: list[dict[str, Any]]) -> dict[str, int]:
    """Bulk import transactions."""
    count = transaction_service.bulk_import_transactions(rows)
    return {"imported_count": count}
