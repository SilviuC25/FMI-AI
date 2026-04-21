from repository.person_repo import PersonRepository
from repository.event_repo import EventRepository
from repository.registration_repo import RegistrationRepository
from domain.person import Person
from domain.event import Event
from domain.validator import PersonValidator, EventValidator
from service.person_service import PersonService
from service.event_service import EventService
import datetime

def test_event_service_get_all_events():
  event_repo = EventRepository()
  reg_repo = RegistrationRepository()
  person_repo = PersonRepository()
  ev_validator = EventValidator()
  es = EventService(event_repo, ev_validator, reg_repo, person_repo)

  e1 = Event("a1", "2025-01-01", "10:00", "Alpha")
  e2 = Event("b2", "2025-02-02", "11:00", "Beta")
  event_repo.add_event_to_repo(e1)
  event_repo.add_event_to_repo(e2)

  all_events = es.get_all_events()
  assert isinstance(all_events, list)
  assert len(all_events) == 2
  assert all_events[0] == e1
  assert all_events[1] == e2

def test_person_service_get_all_people():
  p_repo = PersonRepository()
  ev_repo = EventRepository()
  reg_repo = RegistrationRepository()
  pv = PersonValidator()
  ps = PersonService(p_repo, pv, reg_repo, ev_repo)

  p1 = Person("1000000000000", "Anna")
  p2 = Person("1000000000001", "Ben")
  p_repo.add_person_to_repo(p1)
  p_repo.add_person_to_repo(p2)

  people = ps.get_all_people()
  assert isinstance(people, list)
  assert len(people) == 2
  assert people[0] == p1
  assert people[1] == p2

def test_person_service_get_events_for_person_and_sorts():
  p_repo = PersonRepository()
  ev_repo = EventRepository()
  reg_repo = RegistrationRepository()
  pv = PersonValidator()
  ps = PersonService(p_repo, pv, reg_repo, ev_repo)

  person = Person("2000000000000", "Carol")
  p_repo.add_person_to_repo(person)

  e1 = Event("e1", "2025-03-01", "09:00", "Zoo visit")
  e2 = Event("e2", "2025-01-01", "08:00", "Alpha meeting")
  e3 = Event("e3", "2025-02-01", "10:00", "Ball")
  ev_repo.add_event_to_repo(e1)
  ev_repo.add_event_to_repo(e2)
  ev_repo.add_event_to_repo(e3)

  ev_repo.find_event_by_id = ev_repo.get_event_by_id

  reg_repo.register_person_to_event("2000000000000", "e1", datetime.datetime(2025,3,1,9,0))
  reg_repo.register_person_to_event("2000000000000", "e2", datetime.datetime(2025,1,1,8,0))
  reg_repo.register_person_to_event("2000000000000", "e3", datetime.datetime(2025,2,1,10,0))

  events = ps.get_events_for_person("2000000000000")
  assert len(events) == 3

  sorted_desc = ps.get_events_for_person_sorted_by_description("2000000000000")
  descriptions = [e.get_description() for e in sorted_desc]
  assert descriptions == sorted(descriptions)

  sorted_date = ps.get_events_for_person_sorted_by_date("2000000000000")
  dates = [e.get_date() for e in sorted_date]
  assert dates == sorted(dates)

def test_person_service_top_3_participants():
  p_repo = PersonRepository()
  ev_repo = EventRepository()
  reg_repo = RegistrationRepository()
  pv = PersonValidator()
  ps = PersonService(p_repo, pv, reg_repo, ev_repo)

  p1 = Person("p1p1p1p1p1p1p", "One")
  p2 = Person("p2p2p2p2p2p2p", "Two")
  p3 = Person("p3p3p3p3p3p3p", "Three")
  p4 = Person("p4p4p4p4p4p4p", "Four")
  p_repo.add_person_to_repo(p1)
  p_repo.add_person_to_repo(p2)
  p_repo.add_person_to_repo(p3)
  p_repo.add_person_to_repo(p4)

  ev_repo.add_event_to_repo(Event("ev1", "2025-01-01", "10:00", "E1"))
  ev_repo.add_event_to_repo(Event("ev2", "2025-01-02", "10:00", "E2"))
  ev_repo.add_event_to_repo(Event("ev3", "2025-01-03", "10:00", "E3"))

  reg_repo.register_person_to_event("p1p1p1p1p1p1p", "ev1")
  reg_repo.register_person_to_event("p1p1p1p1p1p1p", "ev2")
  reg_repo.register_person_to_event("p1p1p1p1p1p1p", "ev3")
  reg_repo.register_person_to_event("p2p2p2p2p2p2p", "ev1")
  reg_repo.register_person_to_event("p2p2p2p2p2p2p", "ev2")
  reg_repo.register_person_to_event("p3p3p3p3p3p3p", "ev1")
  reg_repo.register_person_to_event("p4p4p4p4p4p4p", "ev2")

  top3 = ps.get_top_3_participants()
  assert len(top3) == 3
  assert top3[0][0] == p1 and top3[0][1] == 3
  assert top3[1][0] == p2 and top3[1][1] == 2
  assert top3[2][0] == p3 and top3[2][1] == 1

def test_person_service_top_20_percent_events():
  p_repo = PersonRepository()
  ev_repo = EventRepository()
  reg_repo = RegistrationRepository()
  pv = PersonValidator()
  ps = PersonService(p_repo, pv, reg_repo, ev_repo)

  e1 = Event("a", "2025-01-01", "10:00", "A")
  e2 = Event("b", "2025-01-02", "10:00", "B")
  e3 = Event("c", "2025-01-03", "10:00", "C")
  e4 = Event("d", "2025-01-04", "10:00", "D")
  e5 = Event("e", "2025-01-05", "10:00", "E")
  ev_repo.add_event_to_repo(e1)
  ev_repo.add_event_to_repo(e2)
  ev_repo.add_event_to_repo(e3)
  ev_repo.add_event_to_repo(e4)
  ev_repo.add_event_to_repo(e5)

  ev_repo.find_event_by_id = ev_repo.get_event_by_id

  reg_repo.register_person_to_event("x1", "a")
  reg_repo.register_person_to_event("x2", "a")
  reg_repo.register_person_to_event("x3", "b")
  reg_repo.register_person_to_event("x4", "b")
  reg_repo.register_person_to_event("x5", "b")
  reg_repo.register_person_to_event("x6", "c")

  top_events = ps.get_top_20_percent_events()
  assert isinstance(top_events, list)
  assert len(top_events) == 1
  top_event, count = top_events[0]
  assert top_event == e2 and count == 3

def test_integration_event_and_person_services():
  p_repo = PersonRepository()
  ev_repo = EventRepository()
  reg_repo = RegistrationRepository()
  pv = PersonValidator()
  evv = EventValidator()

  ps = PersonService(p_repo, pv, reg_repo, ev_repo)
  es = EventService(ev_repo, evv, reg_repo, p_repo)

  p = Person("9000000000000", "Integrated")
  e = Event("ev900", "2025-12-12", "12:12", "Finale")
  p_repo.add_person_to_repo(p)
  ev_repo.add_event_to_repo(e)
  ev_repo.find_event_by_id = ev_repo.get_event_by_id

  reg_repo.register_person_to_event("9000000000000", "ev900", datetime.datetime(2025,12,1,9,0))

  people = ps.get_all_people()
  events = es.get_all_events()
  assert len(people) == 1 and people[0] == p
  assert len(events) == 1 and events[0] == e
  person_events = ps.get_events_for_person("9000000000000")
  assert len(person_events) == 1 and person_events[0] == e

def run_all_service_tests():
  test_event_service_get_all_events()
  test_person_service_get_all_people()
  test_person_service_get_events_for_person_and_sorts()
  test_person_service_top_3_participants()
  test_person_service_top_20_percent_events()
  test_integration_event_and_person_services()
  print("All service tests passed!")

if __name__ == "__main__":
  run_all_service_tests()