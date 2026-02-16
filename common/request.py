# -*- coding: utf-8 -*-
"""
HTTP Request Wrapper for API Automation Testing
Encapsulates GET/POST/PUT methods with standardized headers and error handling
Added login method to dynamically obtain valid authentication Token
Adapted for execution in GitHub Actions environment
"""
import requests
import time
from config.config import COMMON_HEADERS, REQUEST_TIMEOUT, SSL_VERIFY, URL, TEST_USERNAME, TEST_PASSWORD

# Disable urllib3 insecure request warnings (for SSL verification disabled)
requests.packages.urllib3.disable_warnings()


class HttpRequest:
    """
    Encapsulates HTTP GET, POST, PUT methods and login logic with common headers handling
    All configurations are loaded from config file for environment adaptability
    """

    @staticmethod
    def get(url, headers=None, params=None, verify=None, timeout=None):
        """
        Send HTTP GET request with merged common headers

        Args:
            url (str): Target API URL
            headers (dict, optional): Custom headers to override common headers
            params (dict, optional): URL query parameters
            verify (bool, optional): SSL certificate verification flag (default: SSL_VERIFY from config)
            timeout (int, optional): Request timeout in seconds (default: REQUEST_TIMEOUT from config)

        Returns:
            requests.Response: HTTP response object

        Raises:
            Exception: If GET request execution fails
        """
        # Merge common headers with custom headers
        final_headers = COMMON_HEADERS.copy()
        if headers:
            final_headers.update(headers)

        # Use config defaults if parameters not provided
        final_verify = verify if verify is not None else SSL_VERIFY
        final_timeout = timeout if timeout is not None else REQUEST_TIMEOUT

        try:
            response = requests.get(
                url=url,
                headers=final_headers,
                params=params,
                verify=final_verify,
                timeout=final_timeout
            )
            return response
        except Exception as e:
            raise Exception(f"GET request failed - URL: {url}, Error: {str(e)}")

    @staticmethod
    def post(url, headers=None, params=None, json=None, verify=None, timeout=None):
        """
        Send HTTP POST request with merged common headers

        Args:
            url (str): Target API URL
            headers (dict, optional): Custom headers to override common headers
            params (dict, optional): URL query parameters
            json (dict, optional): JSON-formatted request body (added for common POST use case)
            verify (bool, optional): SSL certificate verification flag (default: SSL_VERIFY from config)
            timeout (int, optional): Request timeout in seconds (default: REQUEST_TIMEOUT from config)

        Returns:
            requests.Response: HTTP response object

        Raises:
            Exception: If POST request execution fails
        """
        # Merge common headers with custom headers
        final_headers = COMMON_HEADERS.copy()
        if headers:
            final_headers.update(headers)

        # Use config defaults if parameters not provided
        final_verify = verify if verify is not None else SSL_VERIFY
        final_timeout = timeout if timeout is not None else REQUEST_TIMEOUT

        try:
            response = requests.post(
                url=url,
                headers=final_headers,
                params=params,
                json=json,  # Added for standard POST JSON body support (non-breaking change)
                verify=final_verify,
                timeout=final_timeout
            )
            return response
        except Exception as e:
            raise Exception(f"POST request failed - URL: {url}, Error: {str(e)}")

    @staticmethod
    def put(url, headers=None, params=None, json=None, verify=None, timeout=None):
        """
        Send HTTP PUT request with merged common headers

        Args:
            url (str): Target API URL
            headers (dict, optional): Custom headers to override common headers
            params (dict, optional): URL query parameters
            json (dict, optional): JSON-formatted request body
            verify (bool, optional): SSL certificate verification flag (default: SSL_VERIFY from config)
            timeout (int, optional): Request timeout in seconds (default: REQUEST_TIMEOUT from config)

        Returns:
            requests.Response: HTTP response object

        Raises:
            Exception: If PUT request execution fails
        """
        # Merge common headers with custom headers
        final_headers = COMMON_HEADERS.copy()
        if headers:
            final_headers.update(headers)

        # Use config defaults if parameters not provided
        final_verify = verify if verify is not None else SSL_VERIFY
        final_timeout = timeout if timeout is not None else REQUEST_TIMEOUT

        try:
            response = requests.put(
                url=url,
                headers=final_headers,
                params=params,
                json=json,
                verify=final_verify,
                timeout=final_timeout
            )
            return response
        except Exception as e:
            raise Exception(f"PUT request failed - URL: {url}, Error: {str(e)}")

    @staticmethod
    def login(url=None, login_data=None, retry_times=2):
        """
        Send login request to dynamically obtain valid authentication Token
        Added retry mechanism to handle occasional login failures

        Args:
            url (str, optional): Login API URL (default: f"{URL}/api/login" from config)
            login_data (dict, optional): Login credentials (default: TEST_USERNAME/TEST_PASSWORD from config)
            retry_times (int, optional): Retry times when login fails (default: 2)

        Returns:
            str: Valid Bearer Token

        Raises:
            Exception: If login fails after all retries or Token not returned
        """
        # Set default values (fallback to config if parameters not provided)
        login_url = url if url else f"{URL}/api/login"
        credentials = login_data if login_data else {
            "email": TEST_USERNAME,
            "password": TEST_PASSWORD
        }

        # Retry logic for robust login
        for attempt in range(retry_times + 1):
            try:
                # Use encapsulated POST method to send login request
                response = HttpRequest.post(url=login_url, json=credentials)
                response.raise_for_status()  # Trigger exception for HTTP error status codes (4xx/5xx)
                res_data = response.json()

                # Verify Token exists in response
                if "token" not in res_data:
                    raise Exception("Login success but no Token returned in response")

                valid_token = res_data["token"]
                print(f"✅ Login successful (attempt {attempt+1}), obtained valid Token: {valid_token}")
                return valid_token

            except Exception as e:
                # Raise final exception if all retries failed
                if attempt == retry_times:
                    raise Exception(f"❌ Login failed after {retry_times+1} attempts - Error: {str(e)}")
                # Retry after short delay
                print(f"⚠️ Login attempt {attempt+1} failed, retrying in 1 second... Error: {str(e)}")
                time.sleep(1)

http = HttpRequest()
