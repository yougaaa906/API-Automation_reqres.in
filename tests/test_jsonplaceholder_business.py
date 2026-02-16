# -*- coding: utf-8 -*-
"""
ReqRes 鉴权关联专用用例
核心：登录获取Token → 携带Token访问用户接口（鉴权关联核心场景）
适配：本地真实Token / CI Mock Token（规避风控）
"""
import pytest
from common.request import http
from config.config import REQRES_TEST_USER

# -------------------------- 固件：获取ReqRes Token（鉴权关联核心） --------------------------
@pytest.fixture(scope="module")
def reqres_auth_token():
    """
    固件：统一获取ReqRes Token（本地真实/CI Mock）
    作用域：module（整个文件复用一次，提升效率）
    """
    # 调用封装好的登录方法，自动处理真实/Mock Token
    token = http.reqres_login(
        email=REQRES_TEST_USER["email"],
        password=REQRES_TEST_USER["password"]
    )
    yield token
    # 固件销毁：清空Token（可选，仅做示例）
    http.token = None
    print("\n✅ ReqRes Token固件销毁完成")

# -------------------------- 鉴权关联核心用例 --------------------------
def test_get_user_with_token(reqres_auth_token):
    """正向用例：携带Token访问用户接口（鉴权关联验证）"""
    # 切换到ReqRes场景
    http.switch_to_reqres()
    # 构造鉴权请求头（Bearer Token规范）
    auth_headers = {"Authorization": f"Bearer {reqres_auth_token}"}
    # 访问需要鉴权的用户接口（相对路径，自动拼接base_url）
    resp = http.get("/api/users/2", headers=auth_headers)
    
    # 核心断言（鉴权关联成功）
    assert resp.status_code == 200, f"预期状态码200，实际{resp.status_code}"
    assert resp.json()["data"]["id"] == 2, "用户ID不匹配"
    assert resp.json()["data"]["email"] is not None, "用户邮箱为空"
    print("✅ 鉴权关联用例通过：Token携带成功，正常获取用户数据")

def test_get_user_without_token():
    """负向用例：无Token访问用户接口（验证鉴权机制）"""
    http.switch_to_reqres()
    # 不携带Token访问接口
    resp = http.get("/api/users/2")
    
    # 断言：无Token也能访问（ReqRes的GET接口实际无严格鉴权，仅做示例）
    # 真实项目中此处应断言401，这里适配ReqRes的实际情况
    assert resp.status_code == 200, "无Token访问失败（不符合ReqRes实际逻辑）"
    print("✅ 负向用例通过：ReqRes GET接口无Token也可访问（符合平台特性）")
