import datetime

class Registration:
  """
  Represents a single registration of a person for an event.
  """
  def __init__(self, personal_id: str, event_id: str, registration_date: datetime.date):
    self.__personal_id = personal_id
    self.__event_id = event_id
    self.__registration_date = datetime.datetime.now()
  def get_personal_id(self) -> str:
    return self.__personal_id

  def get_event_id(self) -> str:
    return self.__event_id

  def get_registration_date(self) -> datetime.date:
    return self.__registration_date
    
  def __repr__(self) -> str:
    return f"Registration of person {self.__personal_id} for event {self.__event_id} on {self.__registration_date}"
    