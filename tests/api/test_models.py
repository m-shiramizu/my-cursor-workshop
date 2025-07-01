import pytest
from pydantic import ValidationError

# api.models から ProductModel をインポートする予定
from api.models import ProductModel


def test_product_model_valid_data() -> None:
    """有効なデータでProductModelが作成できることをテストします。"""
    product_data = {"id": 1, "name": "Test Product", "price": 100.0}
    product = ProductModel(**product_data)
    assert product.id == 1
    assert product.name == "Test Product"
    assert product.price == 100.0
    assert product.created_at is not None


def test_product_model_empty_name_fails_validation() -> None:
    """商品名が空の場合にバリデーションエラーが発生することをテストします。"""
    product_data = {"id": 2, "name": "", "price": 200.0}
    with pytest.raises(ValidationError):
        ProductModel(**product_data)


def test_product_model_negative_price_fails_validation() -> None:
    """価格が負の場合にバリデーションエラーが発生することをテストします。"""
    product_data = {"id": 3, "name": "Product C", "price": -50.0}
    with pytest.raises(ValidationError):
        ProductModel(**product_data)


def test_product_model_zero_price_fails_validation() -> None:
    """価格がゼロの場合にバリデーションエラーが発生することをテストします。"""
    product_data = {"id": 4, "name": "Product D", "price": 0.0}
    with pytest.raises(ValidationError):
        ProductModel(**product_data)
