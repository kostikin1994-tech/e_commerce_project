from unicodedata import category


class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = None
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
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
        result = f'{self.name}, количество продуктов: {len(self.__products)}'

        for product in self.__products:
            result += f'\n{product}'

        return result

    def add_product(self, product):
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        result = ""
        for product in self.__products:
            result += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return result

prod_1 = Product('Макбук', 'Компьютер, который раскладывается и там еще яблоко нарисовано.', 100000, 10)
prod_2 = Product('Айпад', 'Экран от компьютера, который раскладывается и там еще яблоко нарисовано.', 80000, 20)

category = Category('Эппл', 'Электроника, на которой нарисованы яблочки', [prod_1, prod_2])

print(category)

print()

