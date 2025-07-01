from fastapi import FastAPI, HTTPException

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


@app.get("/items/{item_id}", response_model=ProductModel)
async def get_item(item_id: int) -> ProductModel:
    """指定されたIDの商品を取得します。"""
    product = storage.get_product_by_id(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
