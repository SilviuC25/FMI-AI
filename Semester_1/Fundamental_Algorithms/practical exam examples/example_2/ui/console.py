from repository.product_repository import ProductRepository
from service.product_service import ProductService
from domain.product import Product

class Console:
  def __init__(self, product_service: ProductService):
    self.__product_service = product_service

  def print_menu(self):
    print("MODIFY.  Modify the quantity for an existing product")
    print("DISPLAY. Display all the products that have a given string in their name and are not from a given brand")
    print("VALUE. Compute the value of the entire stock")
    print("DELETE. Delete all products with price exceed a given number")

  def handle_modify(self):
    id = int(input("Product ID: "))
    quantity_to_substract = int(input("Quantity to substract: "))

    try:
      self.__product_service.modify_quantity(id, quantity_to_substract)
      print(f"Product {id} modified successfully")
    except ValueError as err:
      print(err)

  def handle_display(self):
    substring = input("Substring: ")
    brand_to_exclude = input("Brand to exclude: ")

    products = self.__product_service.display_products(substring, brand_to_exclude)

    print("The list of products is: ")
    for product in products:
      print(product)

  def handle_value(self):
    value = self.__product_service.stock_value()

    print(f"The value of the entire stock is {value}")

  def handle_delete(self):
    max_price = float(input("Max Price: "))

    try:
      self.__product_service.delete_by_price(max_price)
      print(f"List modified successfully")
    except ValueError as err:
      print(err)

  def run(self):
    while True:
      self.print_menu()
      option = input("Choose an option: ").upper()

      match option:
        case "MODIFY":
          self.handle_modify()

        case "DISPLAY":
          self.handle_display()

        case "VALUE":
          self.handle_value()
        
        case "DELETE":
          self.handle_delete()

        case "STOP":
          break

