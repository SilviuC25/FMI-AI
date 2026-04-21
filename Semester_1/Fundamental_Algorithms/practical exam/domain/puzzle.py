class Puzzle():
  """
  Class Puzzle

  Args:
    id: int, 
    description: str, 
    number_of_pieces: int, 
    price: float
  
  Returns:
    An object Puzzle with given data (id, description, number_of_pieces, price)
  """
  
  def __init__(self, id: int, description: str, number_of_pieces: int, price: float):
    self.__id = id
    self.__description = description
    self.__number_of_pieces = number_of_pieces
    self.__price = price

  def get_id(self):
    return self.__id
  
  def get_description(self):
    return self.__description
  
  def get_number_of_pieces(self):
    return self.__number_of_pieces
  
  def get_price(self):
    return self.__price
  

  def set_id(self, new_id: int):
    self.__id = id
  
  def set_description(self, new_description: str):
    self.__description = new_description
  
  def set_number_of_pieces(self, new_number_of_pieces: int):
    self.__number_of_pieces = new_number_of_pieces
  
  def set_price(self, new_price: float):
    self.__price = new_price


  def __repr__(self):
    return f"{self.get_id()} | {self.get_description()} | {self.get_number_of_pieces()} | {self.get_price()}"
  
  def __str__(self):
    return f"{self.get_id()} | {self.get_description()} | {self.get_number_of_pieces()} | {self.get_price()}"
