class Event:
  """
  Represents an event with an ID, date, time, and description.
  """
  def __init__(self, id: str, date: str, time: str, description: str):
    self.__id = id
    self.__date = date
    self.__time = time
    self.__description = description

  def get_id(self) -> str:
    return self.__id
  
  def get_date(self) -> str:
    return self.__date
  
  def get_time(self) -> str:
    return self.__time
  
  def get_description(self) -> str:
    return self.__description
  
  def set_id(self, id: str):
    self.__id = id

  def set_date(self, date: str):
    self.__date = date
  
  def set_time(self, time: str):
    self.__time = time

  def set_description(self, description: str):
    self.__description = description

  def __repr__(self):
    return f"Event with ID {self.__id}, Date: {self.__date}, Time: {self.__time}, Description: {self.__description}"
  def __eq__(self, other):
    if not isinstance(other, Event):
      return False
    return (self.__id == other.__id)
  
