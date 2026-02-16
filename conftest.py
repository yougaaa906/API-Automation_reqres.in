# -*- coding: utf-8 -*-
"""
Pytest Fixtures for API Automation Testing (Reqres.in)
Provides reusable authentication headers for test cases
Optimized for GitHub Actions execution environment
"""
import pytest
# Import fixed Token from config (only core parameter, no redundancy)
from config.config import FIXED_TOKEN


@pytest.fixture(scope="module")  # Module scope: auth headers created once per test file for efficiency
def get_auth_headers():
    """
    Global authentication fixture for practice phase: Construct auth headers with fixed Token
    All authenticated API test cases can directly use this fixture to carry Token automatically

    Scope: module (created once, reused across all test cases in the same module)
    Yields:
        dict: Authentication headers with Bearer Token (compliant with OAuth 2.0 spec)
    """
    print("\n===== Loading fixed Token auth headers (practice phase) =====")
    # Construct auth headers (follow Bearer spec: Bearer + space + Token)
    auth_headers = {
        "Authorization": f"Bearer {FIXED_TOKEN}"
    }
    print(f"Auth headers constructed successfully: {auth_headers}")
    print("===== Fixed Token auth headers loaded completely =====\n")
    # Pass auth headers to test cases
    yield auth_headers
    # Fixture teardown (optional: no extra operation needed for practice phase)
    print("\n===== All authenticated test cases executed, auth fixture teardown completed =====")