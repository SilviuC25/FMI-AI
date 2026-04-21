class Product:
  def __init__(self, id: int, name: str, brand: str, quantity: int, price: float):
    self.__id = id
    self.__name = name
    self.__brand = brand
    self.__quantity = quantity
    self.__price = price

  def get_id(self):
    return self.__id
  
  def get_name(self):
    return self.__name
  
  def get_brand(self):
    return self.__brand
  
  def get_quantity(self):
    return self.__quantity
  
  def get_price(self):
    return self.__price
  

  def set_id(self, new_id: int):
    self.__id = new_id
  
  def set_name(self, new_name: str):
    self.__name = new_name
  
  def set_brand(self, new_brand: str):
    self.__brand = new_brand
  
  def set_quantity(self, new_quantity: int):
    self.__quantity = new_quantity
  
  def set_price(self, new_price: float):
    self.__price = new_price

  
  def __repr__(self):
    return f"{self.get_id()} | {self.get_name()} | {self.get_brand()} | {self.get_quantity()} | {self.get_price()}"
  
  def __str__(self):
    return f"{self.get_id()} | {self.get_name()} | {self.get_brand()} | {self.get_quantity()} | {self.get_price()}"
  