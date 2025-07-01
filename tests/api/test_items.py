import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# api.mainからappを、api.modelsからProductModelをインポートする予定
from api.main import app

# from api.models import ProductModel # Unused import - removed


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    """テスト用の非同期HTTPクライアントを提供します。"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_product_returns_201(async_client: AsyncClient) -> None:
    """商品作成が成功すると201 Createdを返すことをテストします。"""
    product_data = {"name": "Test Product", "price": 100.0}
    response = await async_client.post("/items", json=product_data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert "name" in response.json()
    assert "price" in response.json()
    assert "created_at" in response.json()


@pytest.mark.asyncio
async def test_create_product_with_valid_data_returns_product(async_client: AsyncClient) -> None:
    """有効なデータで商品を作成し、返された商品情報が正しいことをテストします。"""
    product_data = {"name": "Another Product", "price": 250.50}
    response = await async_client.post("/items", json=product_data)
    response_data = response.json()
    assert response_data["name"] == "Another Product"
    assert response_data["price"] == 250.50


@pytest.mark.asyncio
async def test_create_product_with_empty_name_returns_422(async_client: AsyncClient) -> None:
    """商品名が空の場合に422 Unprocessable Entityを返すことをテストします。"""
    product_data = {"name": "", "price": 100.0}
    response = await async_client.post("/items", json=product_data)
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_create_product_with_negative_price_returns_422(async_client: AsyncClient) -> None:
    """価格が負の場合に422 Unprocessable Entityを返すことをテストします。"""
    product_data = {"name": "Product X", "price": -10.0}
    response = await async_client.post("/items", json=product_data)
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_create_product_with_zero_price_returns_422(async_client: AsyncClient) -> None:
    """価格がゼロの場合に422 Unprocessable Entityを返すことをテストします。"""
    product_data = {"name": "Product Y", "price": 0.0}
    response = await async_client.post("/items", json=product_data)
    assert response.status_code == 422
    assert "detail" in response.json()
