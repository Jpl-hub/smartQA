# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    """测试根路径接口"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# 由于聊天接口需要调用外部API，我们可以添加一个简单的测试
def test_chat_endpoint_exists():
    """测试聊天接口是否存在"""
    # 这个测试只检查接口是否存在，不实际调用API
    response = client.post("/chat", json={"message": ""})
    # 即使消息为空也应该返回错误而不是404
    assert response.status_code != 404
    