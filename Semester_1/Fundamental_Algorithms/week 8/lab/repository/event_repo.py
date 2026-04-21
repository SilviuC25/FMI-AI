from domain.event import Event

class EventRepository:
  def __init__(self):
    self.__events = []

  def add_event_to_repo(self, event: Event):
    """
    Adds an event to the events list.
    Args:
      event (Event): The event to add.
    Returns:
      None
    """
    for e in self.__events:
      if e.get_id() == event.get_id():
        raise ValueError(f"Event with ID {event.get_id()} already exists.")

    self.__events.append(event)

  def get_event_by_id(self, event_id: str) -> Event | None:
    """
    Finds an event by its ID.
    Args:
      event_id (str): The ID of the event to find.
    Returns:
      Event | None: The event if found, None otherwise.
    """
    for event in self.__events:
      if event.get_id() == event_id:
        return event
    return None

  def delete_event_by_id(self, event_id: str) -> bool:
    """
    Deletes an event by its ID.
    Args:
      event_id (str): The ID of the event to delete.
    Returns:
      bool: True if the event was deleted, raises ValueError otherwise.
    """
    event_to_delete = self.get_event_by_id(event_id)
    if event_to_delete is not None:
      self.__events.remove(event_to_delete)
      return True
    else:
      raise ValueError(f"Event with ID {event_id} does not exist.")
  
  def update_event_by_id(self, updated_event: Event) -> bool:
    """
    Updates an existing event.
    Args:
      updated_event (Event): The event with updated information.
    Returns:
      bool: True if the event was updated, False otherwise.
    """
    event_id = updated_event.get_id()

    for e in self.__events:
      if e.get_id() == event_id:
        e.set_date(updated_event.get_date())
        e.set_time(updated_event.get_time())
        e.set_description(updated_event.get_description())
        return True
    else:
      raise ValueError(f"Event with ID {updated_event.get_id()} does not exist.")

  def get_all_events(self) -> list:
    """
    Gets all events from the events list.
    Returns:
      list: A list of all events.
    """
    return self.__events
  
  def get_size(self) -> int:
    """
    Gets the number of events in the repository.
    Returns:
      int: The number of events.
    """
    return len(self.__events)
  
  


  