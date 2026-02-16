# -*- coding: utf-8 -*-
"""
HTTP request wrapper for API automation testing
Features:
- Auto load config params (timeout, headers, base URL)
- Support ReqRes auth association + JSONPlaceholder business association
- CI/local compatibility (mock token fallback)
"""
import requests
from config.config import (
    REQRES_BASE_URL,
    JSONPLACEHOLDER_BASE_URL,
    REQUEST_TIMEOUT,
    SSL_VERIFY,
    COMMON_HEADERS,
    REQRES_MOCK_TOKEN,
    REQRES_TEST_USER
)
from config.log_config import logger

# Disable SSL warnings for test environment
requests.packages.urllib3.disable_warnings()

class HttpRequest:
    def __init__(self):
        """Initialize request object with empty base URL (switch via scenario methods)"""
        self.base_url = ""
        self.headers = COMMON_HEADERS.copy()
        self.token = None  # Store ReqRes auth token

    def reqres_login(self) -> str:
        """
        ReqRes login wrapper: get auth token (real/mock)
        Auto use test account from config, fallback to mock token for CI
        :return: Auth token (real/mock)
        """
        self.base_url = REQRES_BASE_URL
        login_url = "/api/login"
        login_payload = {
            "email": REQRES_TEST_USER["email"],
            "password": REQRES_TEST_USER["password"]
        }

        try:
            resp = self.post(login_url, json=login_payload)
            if resp.status_code == 200:
                self.token = resp.json()["token"]
                logger.info(f"ReqRes login success | Token: {self.token[:8]}...")
                return self.token
            else:
                logger.warning(f"ReqRes login failed (status code {resp.status_code}), use mock token")
                self.token = REQRES_MOCK_TOKEN
                return self.token
        except Exception:
            logger.warning("ReqRes login request exception, use mock token")
            self.token = REQRES_MOCK_TOKEN
            return self.token

    def get(self, url: str, headers: dict = None) -> requests.Response:
        """
        Generic GET request: support full URL/relative path
        :param url: API URL (full/relative)
        :param headers: Custom headers (optional)
        :return: requests.Response
        """
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        try:
            return requests.get(
                url=full_url,
                headers=final_headers,
                timeout=REQUEST_TIMEOUT,
                verify=SSL_VERIFY
            )
        except Exception as e:
            raise Exception(f"GET request failed | URL: {full_url} | Error: {str(e)}")

    def post(self, url: str, json: dict = None, headers: dict = None) -> requests.Response:
        """
        Generic POST request: support full URL/relative path
        :param url: API URL (full/relative)
        :param json: POST payload (JSON format)
        :param headers: Custom headers (optional)
        :return: requests.Response
        """
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        try:
            return requests.post(
                url=full_url,
                json=json,
                headers=final_headers,
                timeout=REQUEST_TIMEOUT,
                verify=SSL_VERIFY
            )
        except Exception as e:
            raise Exception(f"POST request failed | URL: {full_url} | Error: {str(e)}")

 
    def switch_to_reqres(self):
        """Switch base URL to ReqRes environment"""
        self.base_url = REQRES_BASE_URL
        logger.info(f"Switched to ReqRes base URL: {self.base_url}")

    def switch_to_jsonplaceholder(self):
        """Switch base URL to JSONPlaceholder environment"""
        self.base_url = JSONPLACEHOLDER_BASE_URL
        logger.info(f"Switched to JSONPlaceholder base URL: {self.base_url}")
    # -------------------------------------------------------------------

# Global request instance (import and use directly in test cases)
http = HttpRequest()
