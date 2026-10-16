
import pytest
from src.main import Product, Category


@pytest.fixture
def reset_category_count():
    Category.category_count = 0
    Category.product_count = 0


# Тесты Product

def test_product():
    product = Product("Телефон", "Описание", 1000.0, 5)

    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 1000.0
    assert product.quantity == 5


def test_new_product():
    data = {
        "name": "Телефон",
        "description": "Описание",
        "price": 1000.0,
        "quantity": 5,
    }

    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "Телефон"
    assert product.price == 1000.0


def test_price_setter():
    product = Product("Телефон", "Описание", 1000.0, 5)

    product.price = 1500.0

    assert product.price == 1500.0


def test_invalid_price(capsys):
    product = Product("Телефон", "Описание", 1000.0, 5)

    product.price = 0

    assert product.price == 1000.0
    assert (
        "Цена не должна быть нулевая или отрицательная"
        in capsys.readouterr().out
    )


# Тесты Category

def test_category(reset_category_count):
    category = Category("Смартфоны", "Описание", [])

    assert category.name == "Смартфоны"
    assert category.description == "Описание"
    assert category.products == ""

    assert Category.category_count == 1
    assert Category.product_count == 0


def test_add_product(reset_category_count):
    category = Category("Смартфоны", "Описание", [])
    product = Product("Телефон", "Описание", 1000.0, 5)

    category.add_product(product)

    assert "Телефон" in category.products
    assert Category.product_count == 1


def test_category_products_format(reset_category_count):
    product = Product("Телефон", "Описание", 1000.0, 5)
    category = Category("Смартфоны", "Описание", [product])

    assert (
        category.products
        == "Телефон, 1000.0 руб. Остаток: 5 шт.\n"
    )


def test_duplicate_product():
    existing_product = Product("Телефон", "Описание", 1000.0, 2)

    data = {
        "name": "Телефон",
        "description": "Новое описание",
        "price": 1500.0,
        "quantity": 3,
    }

    result = Product.new_product(data, [existing_product])

    assert result is existing_product
    assert existing_product.quantity == 5
    assert existing_product.price == 1500.0


def test_product_add():
    product_1 = Product('Телефон', 'Описание', 1000, 5)
    product_2 = Product('Планшет', 'Описание', 2000, 3)
    assert product_1 + product_2 == 11000


def test_product_str():
    product = Product('Телефон', 'Описание', 1000, 5)
    assert str(product) == 'Телефон, 1000 руб. Остаток: 5 шт.'


def test_category_str():
    product_1 = Product('Телефон', 'Описание', 1000, 5)
    product_2 = Product('Планшет', 'Описание', 2000, 3)
    products = [product_1, product_2]
    category = Category('Электроника', 'Описание', products)

    assert str(category) == (
        'Электроника, количество продуктов: 2\n'
        'Телефон, 1000 руб. Остаток: 5 шт.\n'
        'Планшет, 2000 руб. Остаток: 3 шт.'
    )
