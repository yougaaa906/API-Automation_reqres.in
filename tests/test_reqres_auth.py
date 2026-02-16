# -*- coding: utf-8 -*-
"""
ReqRes auth association test cases
Core: Login to get token → Access user API with token
Compatibility: Local (real token) / CI (mock token)
"""
import pytest
from common.request import http
from config.config import REQRES_TEST_USER
from config.log_config import logger  # Import logger

@pytest.fixture(scope="module")
def reqres_auth_token():
    """
    Fixture: Get ReqRes auth token (reuse for all test cases in module)
    Scope: module (improve test efficiency)
    :return: Auth token (real/mock)
    """
    token = http.reqres_login()
    yield token
    # Fixture teardown: clear token
    http.token = None
    logger.info("ReqRes token fixture teardown completed")  # Replace print

def test_get_user_with_token(reqres_auth_token):
    """Positive case: Access user API with valid token (auth association)"""
    http.switch_to_reqres()
    auth_headers = {"Authorization": f"Bearer {reqres_auth_token}"}
    resp = http.get("/api/users/2", headers=auth_headers)

    # Core assertions for auth association
    assert resp.status_code == 200, f"Expected status code 200, actual {resp.status_code}"
    assert resp.json()["data"]["id"] == 2, "User ID mismatch"
    assert resp.json()["data"]["email"] is not None, "User email is empty"
    logger.info("Auth association test passed: Token carried successfully, user data retrieved")  # Replace print

def test_get_user_without_token():
    """Negative case: Access user API without token (verify auth mechanism)"""
    http.switch_to_reqres()
    resp = http.get("/api/users/2")

    # Assert 403 (ReqRes actual auth logic)
    assert resp.status_code == 403, "Expected 403 for unauthenticated access (ReqRes actual logic)"
    logger.info("Negative test passed: 403 returned for unauthenticated access, auth mechanism works")  # Replace print
