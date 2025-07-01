"""FastAPI + httpx テストテンプレート (ASGITransport使用).

このファイルは、FastAPIアプリケーションをhttpxでテストする際の
正しいパターンを示すテンプレートです。

重要: httpx 0.27.0以降では、TestClientの代わりにASGITransportを使用する必要があります。
"""

import httpx
import pytest
from httpx import ASGITransport

# テスト対象のアプリケーションをインポート
# 分離デプロイ構造の場合は、context.pyを使用
# from context import api_path
# sys.path.insert(0, str(api_path))
# from main import app


# ASGITransportを使用したテストクライアントの設定
@pytest.fixture
def client() -> None:
    """HTTPXクライアントを作成するフィクスチャ.

    ASGITransportを使用してFastAPIアプリケーションを直接テストします。
    これにより実際のHTTPサーバーを起動せずにテストが可能です。
    """
    # 注意: app変数は実際のFastAPIアプリケーションインスタンスに置き換えてください
    # transport = ASGITransport(app=app)
    # with httpx.Client(transport=transport, base_url="http://test") as client:
    #     yield client
    pass


# 同期テストの例
def test_sync_endpoint_example(client: httpx.Client) -> None:
    """同期エンドポイントのテスト例."""
    # response = client.get("/health")
    # assert response.status_code == 200
    # assert response.json() == {"status": "ok"}
    pass


# 非同期テストの例（anyio使用）
@pytest.mark.anyio
async def test_async_endpoint_example() -> None:
    """非同期エンドポイントのテスト例.

    注意: pytest-asyncioではなくanyioを使用しています。
    これはFastAPIとの互換性のためです。
    """
    # transport = ASGITransport(app=app)
    # async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
    #     response = await client.get("/health")
    #     assert response.status_code == 200
    #     assert response.json() == {"status": "ok"}
    pass


# POSTリクエストのテスト例
def test_post_request_example(client: httpx.Client) -> None:
    """POSTリクエストのテスト例."""
    # test_data = {"name": "テスト商品", "price": 1000}
    # response = client.post("/items", json=test_data)
    # assert response.status_code == 201
    #
    # response_data = response.json()
    # assert response_data["name"] == test_data["name"]
    # assert response_data["price"] == test_data["price"]
    # assert "id" in response_data
    # assert "created_at" in response_data
    pass


# エラーケースのテスト例
def test_validation_error_example(client: httpx.Client) -> None:
    """バリデーションエラーのテスト例."""
    # invalid_data = {"name": "", "price": -100}
    # response = client.post("/items", json=invalid_data)
    # assert response.status_code == 422
    #
    # error_detail = response.json()["detail"]
    # assert len(error_detail) == 2
    # assert any(err["loc"] == ["body", "name"] for err in error_detail)
    # assert any(err["loc"] == ["body", "price"] for err in error_detail)
    pass


# TDDサイクル実践例
class TestTDDExample:
    """TDDサイクルの実践例を示すテストクラス."""

    def test_step1_red_phase(self, client: httpx.Client) -> None:
        """Step 1: Red - 失敗するテストを書く."""
        # 最初は実装がないので失敗する
        # response = client.get("/items/1")
        # assert response.status_code == 200
        pass

    def test_step2_green_phase(self, client: httpx.Client) -> None:
        """Step 2: Green - テストを通す最小限の実装."""
        # 仮実装でテストを通す
        # response = client.get("/items/1")
        # assert response.status_code == 200
        # assert response.json() == {"id": 1, "name": "dummy", "price": 100}
        pass

    def test_step3_refactor_phase(self, client: httpx.Client) -> None:
        """Step 3: Refactor - リファクタリング."""
        # データストアから実際のデータを取得するように改善
        # response = client.get("/items/1")
        # assert response.status_code == 200
        #
        # item = response.json()
        # assert item["id"] == 1
        # assert isinstance(item["name"], str)
        # assert isinstance(item["price"], (int, float))
        pass


# 使用上の注意
"""
1. httpx + ASGITransportパターンの使用
   - httpx 0.27.0以降では、FastAPI TestClientの代わりにASGITransportを使用
   - これにより警告なしでテストが実行可能

2. anyioの使用
   - 非同期テストには@pytest.mark.anyioを使用
   - pytest-asyncioではなくanyioを使用することでFastAPIとの互換性を保つ

3. テストの分割
   - 1つのテストメソッドには1つのアサーション（アサーションルーレット回避）
   - エッジケースは別のテストメソッドとして記述

4. 分離デプロイ構造への対応
   - tests/context.pyを使用してapi/ディレクトリをPythonパスに追加
   - これによりapi/main.pyを正しくインポート可能
"""
