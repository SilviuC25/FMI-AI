from domain.event import Event
from domain.person import Person
from utils import *

class EventValidator:
  def is_valid_event_id(self, event_id: str) -> bool:
    """
    Validates an event ID.
    Args:
      event_id (str): The event ID to validate.
    Returns:
      bool: True if the event ID is valid, raises ValueError otherwise.
    """
    event_id = event_id.strip()

    if not event_id or not isinstance(event_id, str) or (len(event_id) < 5 or not event_id.isdigit()):
      return False
    
    return True

  def is_valid_event_description(self, description: str) -> bool:
    """
    Validates an event description.
    Args:
      description (str): The event description to validate.
    Returns:
      bool: True if the event description is valid, raises ValueError otherwise.
    """
    description = description.strip()

    if not description or not isinstance(description, str) or len(description.strip().split()) < 3:
      return False

    return True

  def validate_event(self, event: Event) -> bool:
    """
    Validates an event object.
    Args:
      event (Event): The event object to validate.
    Returns:
      bool: True if the event is valid, raises ValueError otherwise.
    """
    id = event.get_id()
    date = event.get_date()
    time = event.get_time()
    description = event.get_description()

    if not self.is_valid_event_id(id):
      raise ValueError("Invalid event ID.")
    
    if not str_to_datetime(date, time):
      raise ValueError("Invalid date or time format.")
    
    if not self.is_valid_event_description(description):
      raise ValueError("Invalid event description.")
    
    return True
  

class PersonValidator:
  def is_valid_personal_id(self, personal_id: str) -> bool:
    """
    Validates a personal ID.
    Args:
      personal_id (str): The personal ID to validate.
    Returns:
      bool: True if the personal ID is valid, raises ValueError otherwise.
    """
    personal_id = personal_id.strip()

    if not personal_id or not isinstance(personal_id, str) or (len(personal_id) != 13 or not personal_id.isdigit()):
      return False

    return True

  def is_valid_name(self, name: str) -> bool:
      """
      Validates a person's name.
      Args:
        name (str): The name to validate.
      Returns:
        bool: True if the name is valid, raises ValueError otherwise.
      """
      name = name.strip()

      if not name or not isinstance(name, str) or len(name) < 2:
        return False

      return True

  def validate_person(self, person: Person) -> bool:
    """
    Validates a person object.
    Args:
      person: The person object to validate.
    Returns:
      bool: True if the person is valid, raises ValueError otherwise.
    """
    personal_id = person.get_personal_id()
    name = person.get_name()
    
    if not self.is_valid_personal_id(personal_id):
      raise ValueError("Invalid personal ID.")
    
    if not self.is_valid_name(name):
      raise ValueError("Invalid name.")
    
    return True



  
