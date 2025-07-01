from typing import Dict, Optional

from api.models import ProductModel


class InMemoryStorage:
    """商品をメモリに保存するシンプルなストレージクラス。"""

    def __init__(self) -> None:
        self._products: Dict[int, ProductModel] = {}
        self._next_id = 1

    def create_product(self, product: ProductModel) -> ProductModel:
        """新しい商品をストレージに保存し、IDを割り当てます。"""
        product.id = self._next_id
        self._products[self._next_id] = product
        self._next_id += 1
        return product

    def get_product_by_id(self, product_id: int) -> Optional[ProductModel]:
        """指定されたIDの商品を取得します。存在しない場合はNoneを返します。"""
        return self._products.get(product_id)
