# -*- coding: utf-8 -*-
"""
核心配置文件：统一管理多环境、请求参数、测试账号
适配场景：ReqRes鉴权关联 + JSONPlaceholder业务关联
兼容：本地运行（真实请求）、GitHub Actions（无风控）
"""
import os

# ========================== 1. 环境选择（核心） ==========================
# 优先级：CI环境变量 > 本地默认（test）
# 支持：test（测试环境）/prod（生产环境，仅示例）
TEST_ENV = os.getenv("TEST_ENV", "test")

# ========================== 2. 多环境Base URL配置（双场景适配） ==========================
# 分场景管理Base URL，避免硬编码
BASE_URLS = {
    # ReqRes（鉴权关联）
    "reqres": {
        "test": "https://reqres.in",
        "prod": "https://reqres.in"
    },
    # JSONPlaceholder（业务参数关联）
    "jsonplaceholder": {
        "test": "https://jsonplaceholder.typicode.com",
        "prod": "https://jsonplaceholder.typicode.com"
    }
}

# 快捷获取各场景的Base URL（后续代码直接调用）
REQRES_BASE_URL = BASE_URLS["reqres"][TEST_ENV]
JSONPLACEHOLDER_BASE_URL = BASE_URLS["jsonplaceholder"][TEST_ENV]

# ========================== 3. 请求全局配置（通用） ==========================
# 请求超时时间（秒）：CI环境网络可能慢，设15秒更稳
REQUEST_TIMEOUT = 15
# SSL验证：固定False，适配所有测试接口
SSL_VERIFY = False
# 通用请求头：统一管理，避免重复写
COMMON_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

# ========================== 4. 测试账号/凭证配置（ReqRes鉴权用） ==========================
# ReqRes官方测试账号（100%可用，无风控）
REQRES_TEST_USER = {
    "email": "eve.holt@reqres.in",
    "password": "cityslicka"
}
# CI环境Mock Token（规避ReqRes POST接口风控）
REQRES_MOCK_TOKEN = os.getenv("REQRES_MOCK_TOKEN", "mock_token_123456789")

# ========================== 5. 测试报告配置（CI/本地统一） ==========================
# 报告保存路径：本地/CI一致，方便上传
REPORT_PATH = os.getenv("REPORT_PATH", "./test-report.html")
# 报告样式：独立HTML（无外部依赖，下载后可直接打开）
REPORT_ARGS = "--html={} --self-contained-html".format(REPORT_PATH)
