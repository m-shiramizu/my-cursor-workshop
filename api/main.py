from fastapi import FastAPI

from api.models import ProductModel
from api.storage import InMemoryStorage

app = FastAPI(title="商品管理API")
storage = InMemoryStorage()


@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}


@app.post("/items", response_model=ProductModel, status_code=201)
async def create_item(item: ProductModel) -> ProductModel:
    """新しい商品を登録します。"""
    return storage.create_product(item)
