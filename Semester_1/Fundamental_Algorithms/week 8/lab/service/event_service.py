from domain.event import Event
from domain.validator import EventValidator
from repository.event_repo import EventRepository
from repository.person_repo import PersonRepository
from repository.registration_repo import RegistrationRepository

class EventService:
  def __init__(self, event_repository: EventRepository, validator: EventValidator, registration_repository: RegistrationRepository, person_repository: PersonRepository):
    self.__event_repository = event_repository
    self.__validator = validator
    self.__registration_repository = registration_repository
    self.__person_repository = person_repository
    self.__event_repository = event_repository


  def get_all_events(self):
    """
    Gets all events.
    Returns:
      list: A list of all Event objects.
    """

    return self.__event_repository.get_all_events()
  
  def add_event(self, id: str, date: str, time: str, description: str):
    """
    Adds a new event.
    Args:
      id (str): The ID of the event.
      date (str): The date of the event.
      time (str): The time of the event.
      description (str): The description of the event.
    Returns:
      None
    """
    event = Event(id, date, time, description)
    self.__validator.validate_event(event)
    self.__event_repository.add_event_to_repo(event)

  def delete_event(self, event_id: str):
    """
    Removes an event by event ID.
    Args:
      event_id (str): The ID of the event to remove.
    Returns:
      None
    Raises:
      ValueError: If the event does not exist.
    """
    self.__event_repository.delete_event_by_id(event_id)

  def update_event(self, event_id: str, new_date: str, new_time: str, new_description: str):
    """
    Updates an event's details.
    Args:
      event_id (str): The ID of the event to update.
      new_date (str): The new date for the event.
      new_time (str): The new time for the event.
      new_description (str): The new description for the event.
    Returns:
      None
    Raises:
      ValueError: If the event does not exist.
    """
    updated_event = Event(event_id, new_date, new_time, new_description)
    self.__validator.validate_event(updated_event)
    self.__event_repository.update_event_by_id(updated_event)