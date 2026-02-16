
"""
Configuration file for API automation test (Reqres.in)
Contains environment constants and common request headers
Adapted for GitHub Actions execution environment
"""
import os

# -------------------------- API Base Configuration --------------------------
# API base URL - Priority: GitHub Actions env > hardcoded default
API_BASE_URL = os.getenv("API_BASE_URL", "https://reqres.in")

# Authentication credentials - Priority: GitHub Actions secrets > hardcoded default
# Note: In production, always use GitHub Secrets instead of hardcoding
USERNAME = os.getenv("API_TEST_USERNAME", "yougaaa@163.com")
PASSWORD = os.getenv("API_TEST_PASSWORD", "zhangruijie906")

# Fixed authentication token for API requests
FIXED_TOKEN = os.getenv("API_FIXED_TOKEN", "QpwL5tke4Pnpja7X4")

# -------------------------- Common Request Headers --------------------------
# Standard HTTP headers for all API requests
# Can be overridden by custom headers in specific requests
COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8"
}

# -------------------------- Request Configuration --------------------------
# Default request timeout (seconds) - configurable via GitHub Actions env
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# SSL verification flag - disable for testing environments
SSL_VERIFY = os.getenv("SSL_VERIFY", "False").lower() == "true"