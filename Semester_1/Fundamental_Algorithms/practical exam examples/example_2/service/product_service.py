from repository.product_repository import ProductRepository
from domain.product import Product

class ProductService:
  def __init__(self, product_repository: ProductRepository):
    self.__product_repository = product_repository

  def modify_quantity(self, id: int, quantity_to_substract: int):
    self.__product_repository.modify_quantity(id, quantity_to_substract)
    

  def display_products(self, substring: str, brand_to_exclude: str):
    return self.__product_repository.display_products(substring, brand_to_exclude)

  
  def stock_value(self):
    return self.__product_repository.stock_value()
  

  def delete_by_price(self, max_price: float):
    self.__product_repository.delete_by_price(max_price)

  
  