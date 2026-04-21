class Person:
  """
  Represents a person with a personal ID and name.
  """
  def __init__(self, personal_id: str, name: str):
    self.__personal_id = personal_id
    self.__name = name

  def get_personal_id(self) -> str:
    return self.__personal_id
  
  def get_name(self) -> str:
    return self.__name
  
  def set_personal_id(self, personal_id: str):
    self.__personal_id = personal_id

  def set_name(self, name: str):
    self.__name = name
  
  def __repr__(self):
    return f"Person with ID {self.__personal_id} and Name: {self.__name}"
  
  def __eq__(self, other):
    if not isinstance(other, Person):
      return False
    return self.__personal_id == other.__personal_id
  
  

    