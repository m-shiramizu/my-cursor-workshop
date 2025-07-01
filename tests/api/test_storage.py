from datetime import datetime

import pytest

# api.models から ProductModel を、api.storage から InMemoryStorage をインポートする予定
from api.models import ProductModel
from api.storage import InMemoryStorage


@pytest.fixture
def storage() -> InMemoryStorage:
    """InMemoryStorageの新しいインスタンスをテストごとに提供します。"""
    return InMemoryStorage()


def test_create_product_assigns_id_and_returns_product(storage: InMemoryStorage) -> None:
    """商品が作成され、IDが割り当てられて返されることをテストします。"""
    product_data = ProductModel(id=0, name="New Product", price=100.0, created_at=datetime.now())
    created_product = storage.create_product(product_data)
    assert created_product.id is not None
    assert created_product.id > 0
    assert created_product.name == "New Product"
    assert created_product.price == 100.0
    assert created_product.created_at is not None


def test_get_product_by_existing_id(storage: InMemoryStorage) -> None:
    """既存のIDで商品が取得できることをテストします。"""
    product_data = ProductModel(
        id=0, name="Existing Product", price=200.0, created_at=datetime.now()
    )
    created_product = storage.create_product(product_data)
    retrieved_product = storage.get_product_by_id(created_product.id)
    assert retrieved_product is not None
    assert retrieved_product.id == created_product.id
    assert retrieved_product.name == created_product.name


def test_get_product_by_non_existing_id(storage: InMemoryStorage) -> None:
    """存在しないIDで商品を取得しようとするとNoneが返されることをテストします。"""
    retrieved_product = storage.get_product_by_id(999)
    assert retrieved_product is None
