
import pytest
from src.main import BaseProduct, Product, Category, Smartphone, LawnGrass


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
        'Электроника, количество продуктов: 8\n'
        'Телефон, 1000 руб. Остаток: 5 шт.\n'
        'Планшет, 2000 руб. Остаток: 3 шт.'
    )

def test_product_str():
    product = Product("Samsung", "Телефон", 1000, 5)

    assert str(product) == "Samsung, 1000 руб. Остаток: 5 шт."


def test_product_add():
    product1 = Product("Телефон 1", "Описание", 1000, 2)
    product2 = Product("Телефон 2", "Описание", 2000, 3)

    assert product1 + product2 == 8000


def test_product_add_different_types():
    smartphone = Smartphone(
        "Samsung", "Телефон", 1000, 2, 95.5, "S23", 256, "Серый"
    )
    grass = LawnGrass(
        "Трава", "Для газона", 500, 3, "Россия", "7 дней", "Зелёный"
    )

    with pytest.raises(TypeError):
        smartphone + grass


def test_category_str():
    product1 = Product("Телефон 1", "Описание", 1000, 2)
    product2 = Product("Телефон 2", "Описание", 2000, 3)
    category = Category("Телефоны", "Мобильные телефоны", [product1, product2])

    expected = (
        "Телефоны, количество продуктов: 5\n"
        "Телефон 1, 1000 руб. Остаток: 2 шт.\n"
        "Телефон 2, 2000 руб. Остаток: 3 шт."
    )

    assert str(category) == expected


def test_category_add_invalid_product():
    category = Category("Телефоны", "Мобильные телефоны", [])

    with pytest.raises(TypeError):
        category.add_product("Это не товар")


def test_smartphone_initialization():
    smartphone = Smartphone(
        "Samsung", "Телефон", 1000, 2, 95.5, "S23", 256, "Серый"
    )

    assert smartphone.name == "Samsung"
    assert smartphone.price == 1000
    assert smartphone.quantity == 2
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_initialization():
    grass = LawnGrass(
        "Трава", "Для газона", 500, 3, "Россия", "7 дней", "Зелёный"
    )

    assert grass.name == "Трава"
    assert grass.price == 500
    assert grass.quantity == 3
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зелёный"


def test_base_product_is_abstract():
    # Абстрактный класс нельзя создать напрямую.
    with pytest.raises(TypeError):
        BaseProduct("Телефон", "Описание", 1000, 5)


def test_product_inherits_base_product():
    # Проверяем наследование Product от BaseProduct.
    product = Product("Телефон", "Описание", 1000, 5)

    assert isinstance(product, BaseProduct)


def test_mixin_logs_product_creation(capsys):
    # Создаём товар и перехватываем вывод в консоль.
    Product("Телефон", "Описание", 1000, 5)

    captured = capsys.readouterr()

    assert "Product" in captured.out
    assert "Телефон" in captured.out
    assert "Описание" in captured.out
    assert "1000" in captured.out
    assert "5" in captured.out


def test_product_repr():
    product = Product("Телефон", "Описание", 1000, 5)

    result = repr(product)

    assert "Product" in result
    assert "Телефон" in result
    assert "Описание" in result


def test_smartphone_inherits_base_product():
    smartphone = Smartphone(
        "Samsung", "Телефон", 1000, 2, 95.5, "S23", 256, "Серый"
    )

    assert isinstance(smartphone, BaseProduct)


def test_lawn_grass_inherits_base_product():
    grass = LawnGrass(
        "Трава", "Для газона", 500, 3, "Россия", "7 дней", "Зелёный"
    )

    assert isinstance(grass, BaseProduct)

