# -*- coding: utf-8 -*-
"""
API Automation Test Cases for Reqres.in
Covers authentication, CRUD operations with positive/negative scenarios
Adapted for execution in GitHub Actions environment
"""
# Import encapsulated HTTP request object (core for all API calls)
from common.request import http
# Import base URL from config (for API endpoint concatenation)
from config.config import URL

# ===================== Test Case 1: Get Single User with Valid Token (Positive Scenario) =====================
def test_get_single_user_with_valid_token(get_auth_headers):
    """
    Test Description: Access single user API with valid global Token for authentication
    Reuse: get_auth_headers fixture (auto-injects Token) from conftest.py, http.get from common/request.py
    Assertions: Status code 200 + core user data in response + data consistency
    """
    # Concatenate full API URL (configurable base URL + endpoint, easy env switching via config.py)
    api_url = f"{URL}/api/users/2"
    # Call encapsulated GET request with global auth headers (merges common headers + Token header automatically)
    response = http.get(url=api_url, headers=get_auth_headers)
    # Parse response data for assertions
    res_data = response.json()

    # Core assertions (mandatory for API automation: status code + key fields + specific values)
    assert response.status_code == 200, f"Auth access failed! Expected status code 200, actual {response.status_code}"
    assert "data" in res_data, "Core user data field 'data' not found in response"
    assert res_data["data"]["id"] == 2, f"User ID mismatch! Expected 2, actual {res_data['data']['id']}"
    assert res_data["data"]["email"] is not None, "User email field is missing"
    print("✅ Test Case 1 Passed: Access single user API with valid Token works correctly")

# ===================== Test Case 2: Get Single User without Token (Negative Scenario) =====================
def test_get_single_user_without_token():
    """
    Test Description: Access authenticated API without any Token
    Reuse: Only encapsulated HTTP request object, no auth headers (uses common headers by default)
    Assertions: Status code 401 (Unauthorized, compliant with API auth specs)
    """
    api_url = f"{URL}/api/users/2"
    # Call GET request directly without auth headers
    response = http.get(url=api_url)

    # Negative scenario assertion: Verify auth interception works
    assert response.status_code == 401, f"Unauthorized interception failed! Expected status code 401, actual {response.status_code}"
    print("✅ Test Case 2 Passed: Access without Token triggers 401 Unauthorized as expected")

# ===================== Test Case 3: Get Single User with Invalid Token (Boundary Scenario) =====================
def test_get_single_user_with_invalid_token():
    """
    Test Description: Access authenticated API with forged invalid Token
    Reuse: Encapsulated HTTP request object, manually constructed invalid auth headers
    Assertions: Status code 401 (invalid Token should be intercepted)
    """
    api_url = f"{URL}/api/users/2"
    # Construct invalid Token auth headers (valid format, invalid content - simulate real abnormal scenario)
    invalid_auth_headers = {"Authorization": "Bearer invalid_token_123456"}
    # Call GET request with invalid auth headers
    response = http.get(url=api_url, headers=invalid_auth_headers)

    # Boundary scenario assertion: Verify invalid Token is intercepted correctly
    assert response.status_code == 401, f"Invalid Token interception failed! Expected status code 401, actual {response.status_code}"
    print("✅ Test Case 3 Passed: Access with invalid Token triggers 401 Unauthorized as expected")

# ===================== Test Case 4: Create User (Non-Authenticated POST Request) =====================
def test_create_user_without_auth():
    """
    Test Description: Access non-authenticated create user API (POST request with JSON data)
    Reuse: post method of encapsulated HTTP request object, only common headers
    Assertions: Status code 201 (standard code for creation success) + creation result + unique ID
    """
    api_url = f"{URL}/api/users"
    # Construct POST request parameters (dictionary format, auto-converted to JSON in request.py)
    create_data = {
        "name": "auto_test_qa",
        "job": "automation_engineer"
    }
    # Call encapsulated POST request with API URL + request parameters
    response = http.post(url=api_url, json=create_data)
    res_data = response.json()

    # Core assertions: Standard verification for creation success
    assert response.status_code == 201, f"User creation failed! Expected status code 201, actual {response.status_code}"
    assert "id" in res_data, "Unique ID not returned for created user"
    assert res_data["name"] == create_data["name"], "Created username mismatch with request parameters"
    assert res_data["job"] == create_data["job"], "Created user job mismatch with request parameters"
    print(f"✅ Test Case 4 Passed: User created successfully, User ID: {res_data['id']}")

# ===================== Test Case 5: Update User with Valid Token (Positive Scenario, PUT Request) =====================
def test_update_user_with_valid_token(get_auth_headers):
    """
    Test Description: Update user info with valid Token authentication (PUT request)
    Reuse: Global auth headers + put method of encapsulated HTTP request object
    Assertions: Status code 200 + updated data matches request parameters
    """
    api_url = f"{URL}/api/users/2"
    # Construct update parameters (dictionary format)
    update_data = {
        "name": "updated_test_name",
        "job": "updated_automation_tester"
    }
    # Call encapsulated PUT request with auth headers + update parameters
    response = http.put(url=api_url, headers=get_auth_headers, json=update_data)
    res_data = response.json()

    # Core assertions: Verification for update success
    assert response.status_code == 200, f"User update failed! Expected status code 200, actual {response.status_code}"
    assert res_data["name"] == update_data["name"], "Username update not effective"
    assert res_data["job"] == update_data["job"], "User job update not effective"
    print("✅ Test Case 5 Passed: Update user info with valid Token works correctly")