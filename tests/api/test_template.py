"""FastAPI + httpx テストテンプレート.

このファイルは新しいテストを作成する際の参考テンプレートです
実際のテストでは、以下のコメントを解除して使用してください
"""

import pytest
from httpx import ASGITransport, AsyncClient

# 実際のテストでは以下のインポートが必要です
# from api.main import app


# 以下はテンプレートコードです。実際のテストでは app を使用してください

"""
@pytest.mark.anyio
async def test_example_get_endpoint() -> None:
    '''GETエンドポイントのテスト例'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/example")
        assert response.status_code == 200
        assert response.json() == {"message": "success"}


@pytest.mark.anyio
async def test_example_post_endpoint() -> None:
    '''POSTエンドポイントのテスト例'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        test_data = {"name": "テスト", "value": 123}
        response = await client.post("/example", json=test_data)
        assert response.status_code == 201
        assert response.json()["name"] == test_data["name"]


@pytest.mark.anyio
async def test_example_error_case() -> None:
    '''エラーケースのテスト例'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 不正なデータでリクエスト
        invalid_data = {"name": ""}  # 空の名前
        response = await client.post("/example", json=invalid_data)
        assert response.status_code == 400
        assert "detail" in response.json()


# Fixtureを使用する場合の例
@pytest.fixture
async def test_client():
    '''テスト用クライアントのfixture'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.anyio
async def test_with_fixture(test_client: AsyncClient) -> None:
    '''Fixtureを使用したテスト例'''
    response = await test_client.get("/health")
    assert response.status_code == 200
"""
