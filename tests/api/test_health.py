import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# api.mainからappをインポートする予定
from api.main import app


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """テスト用の非同期HTTPクライアントを提供します。"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """ヘルスチェックエンドポイントが正しく応答することをテストします。"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
