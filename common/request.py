# -*- coding: utf-8 -*-
import requests
# 导入config配置
from config.config import API_BASE_URL, REQUEST_TIMEOUT, SSL_VERIFY

requests.packages.urllib3.disable_warnings()

class HttpRequest:
    def __init__(self, base_url: str = None):
        # 优先使用传入的base_url，否则用config中的配置
        self.base_url = base_url or API_BASE_URL
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.session_token = None

    def login(self, username: str = None, password: str = None) -> requests.Response:
        """从config读取默认账号，也支持自定义"""
        from config.config import TEST_USERNAME, TEST_PASSWORD
        login_username = username or TEST_USERNAME
        login_password = password or TEST_PASSWORD
        
        login_url = f"{self.base_url}/api/login"
        payload = {
            "userName": login_username,
            "password": login_password
        }
        response = self.post(url=login_url, json=payload)
        if response.status_code == 200:
            self.session_token = response.json().get("token")
            self.headers["Authorization"] = f"Bearer {self.session_token}"
        return response

    def get(self, url: str, headers: dict = None) -> requests.Response:
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        try:
            return requests.get(
                url=url,
                headers=final_headers,
                timeout=REQUEST_TIMEOUT,  # 从config读取超时
                verify=SSL_VERIFY         # 从config读取SSL配置
            )
        except Exception as e:
            raise Exception(f"GET请求失败 - URL: {url}, 错误: {str(e)}")

    def post(self, url: str, json: dict = None, headers: dict = None) -> requests.Response:
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        try:
            return requests.post(
                url=url,
                headers=final_headers,
                json=json,
                timeout=REQUEST_TIMEOUT,
                verify=SSL_VERIFY
            )
        except Exception as e:
            raise Exception(f"POST请求失败 - URL: {url}, 错误: {str(e)}")

# 初始化请求对象（无需传参，自动读取config）
http = HttpRequest()
