from domain.product import Product

class ProductRepository:
  def __init__(self, filename: str):
    self.__products = []
    self.__filename = filename
    self.__load_from_file()

  def add_product(self, product: Product):
    self.__products.append(product)
    self.__save_to_file()

  def get_all_products(self):
    return self.__products
  
  def get_product_by_id(self, id: int):
    for product in self.get_all_products():
      if product.get_id() == id:
        return product
    
    return False
  
  def __load_from_file(self):
    with open(self.__filename, "r") as file:
      for line in file:
        line = line.strip()
        parts = line.split("; ")
        id = int(parts[0])
        name = parts[1]
        brand = parts[2]
        quantity = int(parts[3])
        price = float(parts[4])

        product = Product(id, name, brand, quantity, price)
        self.add_product(product)

  def __save_to_file(self):
    with open(self.__filename, "w") as file:
      for product in self.get_all_products():
        line = (
          f"{product.get_id()}; "
          f"{product.get_name()}; "
          f"{product.get_brand()}; "
          f"{product.get_quantity()}; "
          f"{product.get_price()}\n"
        )
        file.write(line)

  def modify_quantity(self, id: int, quantity_to_substract: int):
    if quantity_to_substract < 0:
      raise ValueError("Quantity to substract cannot be negative")

    product = self.get_product_by_id(id)

    if not product:
      raise ValueError(f"No product with ID {id} found")

    quantity = product.get_quantity()

    if (quantity < quantity_to_substract):
      raise ValueError(f"Quantity to substract cannot be greater than product's quantity")

    product.set_quantity(quantity - quantity_to_substract)
    self.__save_to_file()
    

  def display_products(self, substring: str, brand_to_exclude: str):
    products_to_display = []
    substring = substring.lower()
    brand_to_exclude = brand_to_exclude.lower()

    for product in self.get_all_products():
      name = str(product.get_name()).lower()
      brand = str(product.get_brand()).lower()

      if substring in name and brand != brand_to_exclude:
        products_to_display.append(product)

    return products_to_display

  
  def stock_value(self):
    value = 0.0

    for product in self.get_all_products():
      quantity = product.get_quantity()
      price = product.get_price()

      value = float(value + quantity * price)

    return value
  
  def delete_by_price(self, max_price: float):
    if max_price < 0:
      raise ValueError("Max price must be non-negative")
    
    new_products = []

    for product in self.__products:
      price = product.get_price()
      if price <= max_price:
        new_products.append(product)

    self.__products = new_products
    self.__save_to_file()


