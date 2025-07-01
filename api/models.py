from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    """商品データモデル"""

    id: Optional[int] = Field(None, description="商品ID")
    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")
    created_at: datetime = Field(default_factory=datetime.now)
