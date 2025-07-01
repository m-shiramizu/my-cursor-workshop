from fastapi import FastAPI

app = FastAPI(title="商品管理API")


@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}
