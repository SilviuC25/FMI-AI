class Task:
  def __init__(self, id: int, title: str, programmer: str, status: str, priority: int):
    self.__id = id
    self.__title = title
    self.__programmer = programmer
    self.__status = status
    self.__priority = priority
  
  def get_id(self):
    return self.__id
  
  def get_title(self):
    return self.__title
  
  def get_programmer(self):
    return self.__programmer
  
  def get_status(self):
    return self.__status
  
  def get_priority(self):
    return self.__priority
  

  def set_id(self, new_id: int):
    self.__id = new_id
  
  def set_title(self, new_title: str):
    self.__title = new_title
  
  def set_programmer(self, new_programmer: str):
    self.__programmer = new_programmer
  
  def set_status(self, new_status: str):
    self.__status = new_status
  
  def set_priority(self, new_priority: int):
    self.__priority = new_priority


  def __repr__(self):
    return f"{self.get_id()} | {self.get_title()} | {self.get_programmer()} | {self.get_status()} | {self.get_priority()}"
  
  def __str__(self):
    return f"{self.get_id()} | {self.get_title()} | {self.get_programmer()} | {self.get_status()} | {self.get_priority()}"
  