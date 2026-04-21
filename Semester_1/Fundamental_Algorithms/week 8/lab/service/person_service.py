from domain.person import Person
from domain.validator import PersonValidator
from repository.person_repo import PersonRepository
from repository.registration_repo import RegistrationRepository
from repository.event_repo import EventRepository

class PersonService:
  def __init__(self, person_repository: PersonRepository, person_validator: PersonValidator, registration_repository: RegistrationRepository, event_repository: EventRepository):
    self.__person_repository = person_repository
    self.__person_validator = person_validator
    self.__registration_repository = registration_repository
    self.__event_repository = event_repository

  def get_all_people(self):
    """
    Gets all people.
    Returns:
      list: A list of all Person objects.
    """
    return self.__person_repository.get_all_people()
  
  def add_person(self, personal_id: str, name: str):
    """
    Adds a new person.
    Args:
      personal_id (str): The personal ID of the person.
      name (str): The name of the person.
    Returns:
      None
    Raises:
      ValueError: If a person with the same ID already exists.
    """
    person = Person(personal_id, name)
    self.__person_repository.add_person_to_repo(person)
    self.__person_validator.validate_person(person)

  def delete_person(self, personal_id: str):
    """
    Removes a person by personal ID.
    Args:
      personal_id (str): The personal ID of the person to remove.
    Returns:
      None
    Raises:
      ValueError: If the person does not exist.
    """
    self.__person_repository.delete_person_by_id(personal_id)

  def update_person(self, personal_id: str, new_name: str):
    """
    Updates a person's name.
    Args:
      personal_id (str): The personal ID of the person to update.
      new_name (str): The new name for the person.
    Returns:
      None
    Raises:
      ValueError: If the person does not exist.
    """
    updated_person = Person(personal_id, new_name)
    self.__person_validator.validate_person(updated_person)
    self.__person_repository.update_person_by_id(updated_person)


  def get_events_for_person(self, personal_id: str):
    """
    Get all events a person participates in.
    Args:
      personal_id (str): The personal ID of the person.
    Returns:
      list: A list of Event objects the person participates in.
    """
    event_ids = self.__registration_repository.get_events_for_person(personal_id)
    return [self.__event_repository.get_event_by_id(eid) for eid in event_ids]

  def get_events_for_person_sorted_by_description(self, personal_id: str):
    """
    Get events sorted alphabetically by description.
    Args:
      personal_id (str): The personal ID of the person.
    Returns:
      list: A list of Event objects sorted by description.
    """
    events = self.get_events_for_person(personal_id)
    return sorted(events, key=lambda e: e.get_description())

  def get_events_for_person_sorted_by_date(self, personal_id: str):
    """Get events sorted by date.
    Args:
      personal_id (str): The personal ID of the person.
    Returns:
      list: A list of Event objects sorted by date.
    """
    events = self.get_events_for_person(personal_id)
    return sorted(events, key=lambda e: e.get_date())

  def get_top_3_participants(self):
    """
    Get top 3 persons participating in most events.
    Returns:
      list: A list of tuples (Person, event_count) for the top 3 participants.
    """
    all_registrations = self.__registration_repository.get_all_registrations()
    person_count = {}
    for personal_id, _, _ in all_registrations:
      person_count[personal_id] = person_count.get(personal_id, 0) + 1
    
    top_3 = sorted(person_count.items(), key=lambda x: x[1], reverse=True)[:3]
    return [(self.__person_repository.get_person_by_id(pid), count) for pid, count in top_3]

  def get_top_20_percent_events(self):
    """
    Get top 20% of events with most participants.
    Returns:
      list: A list of tuples (Event, participant_count) for the top 20% events.
    """
    all_events = self.__event_repository.get_all_events()
    total_events = len(all_events)
    top_20_percent_count = max(1, int(total_events * 0.2))

    event_participants_by_id = {}
    for event in all_events:
      participants = self.__registration_repository.get_participants_for_event(event.get_id())
      event_participants_by_id[event.get_id()] = len(participants)

    sorted_by_count = sorted(event_participants_by_id.items(), key=lambda x: x[1], reverse=True)[:top_20_percent_count]
    top_events = [(self.__event_repository.get_event_by_id(event_id), count) for event_id, count in sorted_by_count]
    return top_events