import datetime

class RegistrationRepository:
  def __init__(self):
    self.__registrations = []

  def register_person_to_event(self, personal_id: str, event_id: str, registration_date: datetime.datetime = None) -> bool:
    """
    Adds a registration of a person to an event.
    Args:
      personal_id (str): The personal ID (CNP) of the person.
      event_id (str): The ID of the event.
      registration_date (datetime.datetime, optional): The registration timestamp. Defaults to current date and time.
    Returns:
      bool: True if registration was successful, False if person is already registered.
    """
    if registration_date is None:
      registration_date = datetime.datetime.now()
    if self._is_registered(personal_id, event_id):
      return False
    self.__registrations.append((personal_id, event_id, registration_date))
    return True

  def _is_registered(self, personal_id: str, event_id: str) -> bool:
    """
    Checks if a person is already registered for a specific event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      bool: True if the person is registered for the event, False otherwise.
    """
    return any(pid == personal_id and eid == event_id for pid, eid, _ in self.__registrations)

  def get_events_for_person(self, personal_id: str) -> list:
    """
    Gets all event IDs that a person is registered for.
    Args:
      personal_id (str): The personal ID of the person.
    Returns:
      list: A list of event IDs the person is registered to.
    """
    return [eid for pid, eid, _ in self.__registrations if pid == personal_id]

  def get_participants_for_event(self, event_id: str) -> list:
    """
    Gets all personal IDs of participants registered for a specific event.
    Args:
      event_id (str): The ID of the event.
    Returns:
      list: A list of personal IDs registered for the event.
    """
    return [pid for pid, eid, _ in self.__registrations if eid == event_id]

  def get_registration_date(self, personal_id: str, event_id: str) -> datetime.datetime:
    """
    Gets the registration date/time for a person and event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      datetime.datetime: The registration timestamp, or None if not registered.
    """
    for pid, eid, rdate in self.__registrations:
      if pid == personal_id and eid == event_id:
        return rdate
    return None

  def unregister_person_from_event(self, personal_id: str, event_id: str) -> bool:
    """
    Removes a person's registration from an event.
    Args:
      personal_id (str): The personal ID of the person.
      event_id (str): The ID of the event.
    Returns:
      bool: True if unregistration was successful, False if person was not registered.
    """
    for i, (pid, eid, _) in enumerate(self.__registrations):
      if pid == personal_id and eid == event_id:
        self.__registrations.pop(i)
        return True
    return False

  def get_all_registrations(self) -> list:
    """
    Gets all registrations in the system.
    Args:
      None
    Returns:
      list: A list of tuples (personal_id, event_id, registration_date).
    """
    return list(self.__registrations)

  def get_size(self) -> int:
    """
    Gets the total number of registrations.
    Args:
      None
    Returns:
      int: The count of all registrations.
    """
    return len(self.__registrations)