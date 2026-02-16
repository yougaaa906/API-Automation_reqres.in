# -*- coding: utf-8 -*-
"""
HTTP Request Wrapper for API Automation Testing
Encapsulates GET/POST methods with standardized headers and error handling
Adapted for execution in GitHub Actions environment
"""
import requests
from config.config import COMMON_HEADERS, REQUEST_TIMEOUT, SSL_VERIFY

# Disable urllib3 insecure request warnings (for SSL verification disabled)
requests.packages.urllib3.disable_warnings()


class HttpRequest:
    """
    Encapsulates HTTP GET and POST methods with common headers handling
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


# Singleton instance for global usage across test scripts
http = HttpRequest()