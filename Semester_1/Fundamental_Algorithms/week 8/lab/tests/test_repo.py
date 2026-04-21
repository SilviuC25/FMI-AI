from repository.person_repo import PersonRepository
from repository.event_repo import EventRepository
from repository.registration_repo import RegistrationRepository
from domain.person import Person
from domain.event import Event
import datetime

def test_person_repo_add_and_get_all():
  repo = PersonRepository()
  p1 = Person("1234567890123", "Alice")
  p2 = Person("9876543210987", "Bob")

  repo.add_person_to_repo(p1)
  repo.add_person_to_repo(p2)

  all_people = repo.get_all_people()
  assert isinstance(all_people, list)
  assert len(all_people) == 2
  assert all_people[0] == p1
  assert all_people[1] == p2

  p_dup = Person("1234567890123", "Alice Dup")
  try:
    repo.add_person_to_repo(p_dup)
    assert False
  except ValueError:
    pass

def test_person_repo_get_person_by_id():
  repo = PersonRepository()
  p = Person("1111111111111", "Charlie")
  repo.add_person_to_repo(p)

  found = repo.get_person_by_id("1111111111111")
  assert found == p

  not_found = repo.get_person_by_id("0000000000000")
  assert not_found is None

def test_person_repo_delete_person_by_id():
  repo = PersonRepository()
  p1 = Person("2000000000000", "David")
  p2 = Person("2000000000001", "Eve")
  repo.add_person_to_repo(p1)
  repo.add_person_to_repo(p2)

  res = repo.delete_person_by_id("2000000000000")
  assert res is True
  assert repo.get_person_by_id("2000000000000") is None
  assert repo.get_size() == 1

  try:
    repo.delete_person_by_id("9999999999999")
    assert False
  except ValueError:
    pass

def test_person_repo_update_person_by_id():
  repo = PersonRepository()
  p = Person("3000000000000", "Frank")
  repo.add_person_to_repo(p)

  updated = Person("3000000000000", "Franklin")
  res = repo.update_person_by_id(updated)
  assert res is True
  found = repo.get_person_by_id("3000000000000")
  assert found.get_name() == "Franklin"

  non_existing = Person("9999999999998", "Ghost")
  try:
    repo.update_person_by_id(non_existing)
    assert False
  except ValueError:
    pass

def test_event_repo_add_and_get_all():
  repo = EventRepository()
  e1 = Event("10000", "2025-01-01", "10:00", "New Year Party")
  e2 = Event("10001", "2025-02-14", "20:00", "Valentine Gala")

  repo.add_event_to_repo(e1)
  repo.add_event_to_repo(e2)

  all_events = repo.get_all_events()
  assert isinstance(all_events, list)
  assert len(all_events) == 2
  assert all_events[0] == e1
  assert all_events[1] == e2

  e_dup = Event("10000", "2025-01-02", "11:00", "Duplicate")
  try:
    repo.add_event_to_repo(e_dup)
    assert False
  except ValueError:
    pass

def test_event_repo_get_event_by_id():
  repo = EventRepository()
  e = Event("20000", "2025-03-01", "09:00", "Meeting")
  repo.add_event_to_repo(e)

  found = repo.get_event_by_id("20000")
  assert found == e

  not_found = repo.get_event_by_id("nope")
  assert not_found is None

def test_event_repo_delete_event_by_id():
  repo = EventRepository()
  e1 = Event("30000", "2025-04-01", "12:00", "April")
  e2 = Event("30001", "2025-05-01", "12:00", "May")
  repo.add_event_to_repo(e1)
  repo.add_event_to_repo(e2)

  res = repo.delete_event_by_id("30000")
  assert res is True
  assert repo.get_event_by_id("30000") is None
  assert repo.get_size() == 1

  try:
    repo.delete_event_by_id("missing")
    assert False
  except ValueError:
    pass

def test_event_repo_update_event_by_id():
  repo = EventRepository()
  e = Event("40000", "2025-06-01", "08:00", "Original")
  repo.add_event_to_repo(e)

  updated = Event("40000", "2025-06-02", "09:00", "Updated")
  res = repo.update_event_by_id(updated)
  assert res is True
  found = repo.get_event_by_id("40000")
  assert found.get_date() == "2025-06-02"
  assert found.get_time() == "09:00"
  assert found.get_description() == "Updated"

  non_existing = Event("zzz", "2025-01-01", "00:00", "None")
  try:
    repo.update_event_by_id(non_existing)
    assert False
  except ValueError:
    pass

def test_registration_repo_full_flow():
  repo = RegistrationRepository()
  now = datetime.datetime.now()
  ok = repo.register_person_to_event("p1", "e1", registration_date=now)
  assert ok is True
  ok_dup = repo.register_person_to_event("p1", "e1")
  assert ok_dup is False
  assert repo._is_registered("p1", "e1") is True

  events_for_p1 = repo.get_events_for_person("p1")
  assert events_for_p1 == ["e1"]

  participants_for_e1 = repo.get_participants_for_event("e1")
  assert participants_for_e1 == ["p1"]

  reg_date = repo.get_registration_date("p1", "e1")
  assert isinstance(reg_date, datetime.datetime)
  assert reg_date == now

  unres = repo.unregister_person_from_event("p1", "e1")
  assert unres is True
  assert repo._is_registered("p1", "e1") is False

  unres2 = repo.unregister_person_from_event("p1", "e1")
  assert unres2 is False

  repo.register_person_to_event("a","X")
  repo.register_person_to_event("b","X")
  all_regs = repo.get_all_registrations()
  assert isinstance(all_regs, list)
  assert repo.get_size() == len(all_regs)

def test_repos_independence():
  person_repo = PersonRepository()
  event_repo = EventRepository()

  p = Person("7777777777777", "Isolated")
  e = Event("ev777", "2025-07-07", "07:07", "Lucky")

  person_repo.add_person_to_repo(p)
  event_repo.add_event_to_repo(e)

  assert person_repo.get_person_by_id("7777777777777") == p
  assert event_repo.get_event_by_id("ev777") == e

def run_all_repo_tests():
  test_person_repo_add_and_get_all()
  test_person_repo_get_person_by_id()
  test_person_repo_delete_person_by_id()
  test_person_repo_update_person_by_id()
  test_event_repo_add_and_get_all()
  test_event_repo_get_event_by_id()
  test_event_repo_delete_event_by_id()
  test_event_repo_update_event_by_id()
  test_registration_repo_full_flow()
  test_repos_independence()
  print("All repository tests passed!")

if __name__ == "__main__":
  run_all_repo_tests()
