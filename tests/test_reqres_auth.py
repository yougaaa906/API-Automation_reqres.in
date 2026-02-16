# -*- coding: utf-8 -*-
"""
Saucedemo API Automation Test Cases
Core: Interface association, positive/negative/boundary scenarios
Compatible with GitHub Actions (no risk control)
"""
from common.request import http
import pytest

# -------------------------- Fixtures (Interface Association Core) --------------------------
@pytest.fixture(scope="module")
def saucedemo_login_token():
    """
    Fixture: Get valid token by logging in saucedemo (base for interface association)
    Use default account from config, ensure global reuse
    """
    # Call login method (auto read account from config)
    response = http.login()
    
    # Core assertions for login success
    assert response.status_code == 200, f"Login failed - Status code: {response.status_code}"
    assert http.session_token is not None, "Token not obtained after login"
    assert len(http.session_token) > 0, "Token is empty string"
    
    # Output login info (for debugging in CI)
    print(f"\n✅ Login success - Token: {http.session_token[:10]}...")
    yield http.session_token

# -------------------------- Test Cases --------------------------
def test_get_products_with_valid_token(saucedemo_login_token):
    """
    Positive Scenario: Get product list with valid token
    Verify interface association and data integrity
    """
    # Construct API URL
    api_url = f"{http.base_url}/inventory-api/item"
    
    # Send GET request (auto carry token in headers)
    response = http.get(url=api_url)
    res_data = response.json()
    
    # Multi-dimensional assertions
    # 1. Status code assertion
    assert response.status_code == 200, f"Expected status code 200, actual: {response.status_code}"
    # 2. Data type assertion
    assert isinstance(res_data, list), f"Product list should be list type, actual: {type(res_data)}"
    # 3. Data non-empty assertion
    assert len(res_data) > 0, "Product list is empty (unexpected)"
    # 4. Core field assertion (verify data integrity)
    core_fields = ["id", "name", "price", "description", "image"]
    for field in core_fields:
        assert field in res_data[0], f"Missing core field '{field}' in product data"
    # 5. Data format assertion (price should be number)
    assert isinstance(res_data[0]["price"], (int, float)), "Product price should be number type"
    
    # Success log
    print(f"✅ Test 1 Passed - Get {len(res_data)} products successfully")

def test_login_with_wrong_password():
    """
    Negative Scenario: Login with wrong password
    Verify authentication error handling
    """
    # Custom wrong password (override config default)
    wrong_password = "wrong_pass_123456"
    response = http.login(password=wrong_password)
    
    # Assertion for authentication failure
    assert response.status_code == 401, f"Expected status code 401, actual: {response.status_code}"
    # Verify token is not generated
    assert http.session_token is None, "Token should be None after failed login"
    
    # Success log
    print("✅ Test 2 Passed - Login with wrong password failed (expected)")

def test_login_with_empty_password():
    """
    Boundary Scenario: Login with empty password
    Verify boundary condition handling
    """
    # Empty password (extreme boundary case)
    response = http.login(password="")
    
    # Assertion for authentication failure
    assert response.status_code == 401, f"Expected status code 401, actual: {response.status_code}"
    
    # Success log
    print("✅ Test 3 Passed - Login with empty password failed (expected)")

def test_login_with_nonexistent_user():
    """
    Negative Scenario: Login with nonexistent username
    Verify user not found handling
    """
    # Nonexistent test account
    nonexistent_user = "nonexistent_user_123456"
    response = http.login(username=nonexistent_user)
    
    # Assertion for authentication failure
    assert response.status_code == 401, f"Expected status code 401, actual: {response.status_code}"
    
    # Success log
    print("✅ Test 4 Passed - Login with nonexistent user failed (expected)")

def test_get_single_product_with_valid_token(saucedemo_login_token):
    """
    Positive Scenario: Get single product detail with valid token
    Verify single resource query
    """
    # First get product list to get valid product ID
    list_url = f"{http.base_url}/inventory-api/item"
    list_response = http.get(url=list_url)
    valid_product_id = list_response.json()[0]["id"]
    
    # Get single product detail
    single_product_url = f"{http.base_url}/inventory-api/item/{valid_product_id}"
    response = http.get(url=single_product_url)
    res_data = response.json()
    
    # Core assertions
    assert response.status_code == 200, f"Expected status code 200, actual: {response.status_code}"
    assert res_data["id"] == valid_product_id, f"Product ID mismatch - Expected: {valid_product_id}, Actual: {res_data['id']}"
    assert res_data["name"] is not None, "Product name is empty"
    
    # Success log
    print(f"✅ Test 5 Passed - Get single product (ID: {valid_product_id}) successfully")
