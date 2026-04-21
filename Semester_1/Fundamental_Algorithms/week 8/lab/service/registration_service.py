import datetime
from repository.registration_repo import RegistrationRepository
from repository.person_repo import PersonRepository
from repository.event_repo import EventRepository

class RegistrationService:
  def __init__(self, registration_repository: RegistrationRepository, person_repository: PersonRepository, event_repository: EventRepository):
    self.__registration_repository = registration_repository
    self.__person_repository = person_repository
    self.__event_repository = event_repository

  def register_person_to_event(self, personal_id: str, event_id: str) -> bool:
    """
    Registers a person for an event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      bool: True if registration was successful, False if already registered.
    Raises:
      ValueError: If person or event does not exist.
    """
    person = self.__person_repository.get_person_by_id(personal_id)
    if person is None:
      raise ValueError(f"Person with ID {personal_id} does not exist.")
    event = self.__event_repository.get_event_by_id(event_id)
    if event is None:
      raise ValueError(f"Event with ID {event_id} does not exist.")
    return self.__registration_repository.register_person_to_event(personal_id, event_id)

  def unregister_person_from_event(self, personal_id: str, event_id: str) -> bool:
    """
    Unregisters a person from an event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      bool: True if unregistration was successful, False if not registered.
    """
    return self.__registration_repository.unregister_person_from_event(personal_id, event_id)

  def is_registered(self, personal_id: str, event_id: str) -> bool:
    """
    Checks if a person is registered for an event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      bool: True if registered, False otherwise.
    """
    return self.__registration_repository._is_registered(personal_id, event_id)

  def get_events_for_person(self, personal_id: str) -> list:
    """
    Gets all events a person is registered for.
    Args:
      personal_id (str): The personal ID of the person.
    Returns:
      list: A list of Event objects.
    """
    event_ids = self.__registration_repository.get_events_for_person(personal_id)
    return [self.__event_repository.get_event_by_id(eid) for eid in event_ids if self.__event_repository.get_event_by_id(eid) is not None]

  def get_participants_for_event(self, event_id: str) -> list:
    """
    Gets all participants for an event.
    Args:
      event_id (str): The ID of the event.
    Returns:
      list: A list of Person objects.
    """
    personal_ids = self.__registration_repository.get_participants_for_event(event_id)
    return [self.__person_repository.get_person_by_id(pid) for pid in personal_ids if self.__person_repository.get_person_by_id(pid) is not None]

  def get_registration_date(self, personal_id: str, event_id: str) -> datetime.datetime:
    """
    Gets the registration date/time for a person and event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      datetime.datetime: The registration timestamp, or None if not registered.
    """
    return self.__registration_repository.get_registration_date(personal_id, event_id)

  def get_all_registrations(self) -> list:
    """
    Gets all registrations in the system.
    Args:
      None
    Returns:
      list: A list of tuples (personal_id, event_id, registration_date).
    """
    return self.__registration_repository.get_all_registrations()

  def get_size(self) -> int:
    """
    Gets the total number of registrations.
    Args:
      None
    Returns:
      int: The count of all registrations.
    """
    return self.__registration_repository.get_size()