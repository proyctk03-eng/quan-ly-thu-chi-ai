"""Application configuration and constants."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)


# ---------------------------------------------------------------------------
# Student expense categories
# ---------------------------------------------------------------------------
STUDENT_CATEGORIES: list[str] = [
    "Ăn uống & Cafe",
    "Tiền nhà & Tiện ích",
    "Học tập & Sách vở",
    "Di chuyển & Xăng xe",
    "Giải trí & Bè bạn",
    "Mua sắm cá nhân",
    "Chu cấp gia đình",
    "Đi làm thêm",
    "Khác",
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DB_FILE: str = os.getenv("DB_FILE", "chi_tieu.db")

# ---------------------------------------------------------------------------
# Gemini API
# ---------------------------------------------------------------------------
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL_NAME: str = "gemini-flash-latest"

GEO_BLOCK_MSG: str = (
    "🌐 **Hệ thống đang bị chặn địa lý (Geo-blocking).**\n\n"
    "Google Gemini API không khả dụng tại vị trí hiện tại của bạn.\n\n"
    "**Cách khắc phục:**\n"
    "1. Bật **VPN** (kết nối tới US/Singapore/Japan)\n"
    "2. Hoặc cấu hình proxy trong file `.env`:\n"
    "```\nHTTP_PROXY=http://your-proxy:port\n"
    "HTTPS_PROXY=http://your-proxy:port\n```\n"
    "3. Khởi động lại ứng dụng sau khi cấu hình."
)


# ---------------------------------------------------------------------------
# Proxy helpers
# ---------------------------------------------------------------------------
def inject_proxy() -> None:
    """Read proxy settings from env and inject into ``os.environ``."""
    load_dotenv(override=True)
    http_proxy = os.getenv("HTTP_PROXY", "").strip()
    https_proxy = os.getenv("HTTPS_PROXY", "").strip()

    if http_proxy:
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["http_proxy"] = http_proxy
    if https_proxy:
        os.environ["HTTPS_PROXY"] = https_proxy
        os.environ["https_proxy"] = https_proxy


def is_geo_blocked_error(error: Exception) -> bool:
    """Return *True* if *error* looks like a Gemini geo-blocking error."""
    error_str = str(error).lower()
    return (
        "location is not supported" in error_str
        or "failed_precondition" in error_str
        or "user location" in error_str
    )
