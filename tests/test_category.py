import pytest
from src.main import Category

@pytest.fixture
def reset_category_count():
    Category.category_count = 0
    Category.product_count = 0

def test_category(reset_category_count):
    category = Category("Смартфоны", "Описание", [])

    assert category.name == "Смартфоны"
    assert category.description == "Описание"
    assert category.products == []

    assert Category.category_count == 1
    assert Category.product_count == 0


