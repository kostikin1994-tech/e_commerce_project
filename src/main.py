
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный родительский класс для продуктов."""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        """Каждый конкретный продукт должен реализовать этот метод."""
        pass


class MixinLog:
    """Выводит информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class Product(MixinLog, BaseProduct):
    """Класс конкретного продукта."""

    def __init__(self, name, description, price, quantity):
        self.__price = None
        if quantity > 0:
            super().__init__(name, description, price, quantity)
        else:
            raise ValueError('Товар с нулевым количеством не может быть добавлен')


    def __str__(self):
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        price_1 = self.price * self.quantity
        price_2 = other.price * other.quantity
        return price_1 + price_2

    @classmethod
    def new_product(cls, product, products=None):
        if products is not None:
            for existing_product in products:
                if existing_product.name == product["name"]:
                    existing_product.quantity += product["quantity"]

                    if product["price"] > existing_product.price:
                        existing_product.price = product["price"]

                    return existing_product

        return cls(**product)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        self.__price = value


class Category:
    category_count = 0
    product_count = 0

    name: str
    description: str

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

        for product in products:
            self.add_product(product)

    def __str__(self):
        result = (
            f'{self.name}, количество продуктов: '
            f'{sum(product.quantity for product in self.__products)}'
        )

        for product in self.__products:
            result += f'\n{product}'

        return result

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError(
                f'Объект типа {type(product).__name__} '
                'не является объектом класса Product.'
            )

    def middle_price(self):
        sum_prod = 0
        count_products = 0
        try:
            for product in self.__products:
                sum_prod += product.price
                count_products += 1
            result = sum_prod / count_products
            return result
        except ZeroDivisionError:
            return 0


    @property
    def products(self):
        result = ""

        for product in self.__products:
            result += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )

        return result


class Smartphone(Product):
    def __init__(
        self, name, description, price, quantity,
        efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self, name, description, price, quantity,
        country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())