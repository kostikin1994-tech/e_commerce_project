import pytest
from src.main import Product

def test_product():
    product = Product("Телефон", "Описание", 1000.0, 5)

    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 1000.0
    assert product.quantity == 5

