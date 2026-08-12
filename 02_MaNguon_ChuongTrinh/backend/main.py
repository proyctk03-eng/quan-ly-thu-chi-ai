"""FastAPI main application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import analytics, ai, budgets, transactions
from backend.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan event: initialize SQLite database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Sổ Tay Quản Lý Chi Tiêu Sinh Viên AI — Backend API",
    description="FastAPI RESTful service for Student Expense Manager & Gemini AI Agent",
    version="2.0.0",
    lifespan=lifespan,
)

# Enable CORS for Streamlit frontend or cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(analytics.router)
app.include_router(ai.router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "FastAPI Backend"}
