
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
        super().__init__(name, description, price, quantity)

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
